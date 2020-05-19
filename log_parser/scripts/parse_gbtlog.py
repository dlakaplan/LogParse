#!/usr/bin/env python
from __future__ import print_function, division
import argparse
import glob
import os
import datetime
import re
import logging
import sys
import json


try:
    from cStringIO import StringIO  # Python 2
except ImportError:
    from io import StringIO

try:
    import urllib.request  # Python 3

    _python3 = True
except:
    import requests

    _python3 = False

from log_parser import log_parser


def main():
    parser = argparse.ArgumentParser(
        description="Parse an GBT log file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--file",
        "-f",
        type=str,
        nargs="+",
        default=None,
        help="Name(s) of GBT log file(s)",
    )
    parser.add_argument(
        "--directory",
        "-d",
        type=str,
        default="./",
        help="Directory to search for log files",
    )
    parser.add_argument(
        "--days",
        "-t",
        type=int,
        default=1,
        help="Days in the past to look for log files (<=0: find all)",
    )
    parser.add_argument(
        "--tolerance",
        type=int,
        default=100,
        help="Tolerance for printing out exposure difference marks",
    )
    # parser.add_argument('--email', '-e',
    #                    type=str,
    #                    default=None,
    #                    help='Send email with results')

    parser.add_argument(
        "--slack",
        "-s",
        action="store_true",
        help="Send results to slack (requires ~/.slackurl)",
    )

    parser.add_argument(
        "--out", "-o", default="stdout", type=str, help="Output destination"
    )
    parser.add_argument(
        "--verbose", "-v", action="count", default=0, help="Increase verbosity"
    )

    args = parser.parse_args()
    if args.verbose == 0:
        log_parser.logger.setLevel(logging.WARNING)
    elif args.verbose == 1:
        log_parser.logger.setLevel(logging.INFO)
    elif args.verbose == 2:
        log_parser.logger.setLevel(logging.DEBUG)

    if args.out == "stdout":
        args.out = sys.stdout
    else:
        args.out = open(args.out, "w")
        # add in a second logger that outputs to the same file as the main output destination
        newhandler = logging.StreamHandler(args.out)
        formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
        newhandler.setFormatter(formatter)
        log_parser.logger.addHandler(newhandler)

    if args.slack:
        slackurl = None
        with open(os.path.join(os.getenv("HOME"), ".slackurl")) as slackfile:
            slackurl = slackfile.read().strip()
        # make another logging handler to store things for slack
        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.INFO)
        slackhandler = logging.StreamHandler(log_stream)
        slackformatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
        slackhandler.setFormatter(slackformatter)
        log_parser.logger.addHandler(slackhandler)

    if args.file is None:
        today = datetime.datetime.today()
        good_files = []
        if args.days > 0:
            log_parser.logger.debug(
                "Looking for files written < %d days ago in %s",
                args.days,
                args.directory,
            )
        else:
            log_parser.logger.debug(
                "Looking for files in %s", args.directory,
            )

        for dir_name, subdir_list, file_list in os.walk(args.directory):
            for file in file_list:
                if re.match(r"\wGBT\d\d[AB]_\d+_\d+_log.txt", file):
                    filename = os.path.join(dir_name, file)
                    modtime = datetime.datetime.fromtimestamp(
                        os.path.getmtime(filename)
                    )
                    if args.days > 0:
                        if today - modtime < datetime.timedelta(days=args.days):
                            good_files.append(filename)
                    else:
                        good_files.append(filename)

        if len(good_files) == 0:
            log_parser.logger.error("No files found")

    else:
        good_files = args.file

    for file in good_files:
        start_line = 0
        logs = []
        while True:
            log = log_parser.GBTPulsarObservationLog.parse_gbt_logfile(
                file, start_line = start_line, tolerance=args.tolerance,
                )
            if log.start_time is None:
                break
            if log.end_line is None:
                log_parser.logger.error(
                    "parser returned end line of None while parsing %s", file
                    )
                break
            start_line = log.end_line + 1
            logs.append(log)

        for log in logs:
            log.print_results(output=args.out)

            if args.slack and slackurl is not None:
                log.print_results(output=log_stream)

    if args.slack:
        text = log_stream.getvalue()
        # do a bit of formatting for slack
        text = text.replace("ERROR", "*ERROR*").replace("WARNING", "_WARNING_")
        text = text.replace("NANOGrav", "*NANOGrav*")
        text = re.sub(r"(\s+)(\wGBT\d\d\w_\d+)", r"\1*\2*", text)

        body = {"username": "GBTbot", "text": text}
        jsondata = json.dumps(body)
        jsondataasbytes = jsondata.encode("utf-8")  # needs to be bytes
        # post it to slack
        if _python3:
            req = urllib.request.Request(slackurl)
            req.add_header("Content-Type", "application/json; charset=utf-8")
            req.add_header("Content-Length", len(jsondataasbytes))
            response = urllib.request.urlopen(req, jsondataasbytes)
        else:
            response = requests.post(
                slackurl, data=jsondata, headers={"Content-Type": "application/json"},
            )

        if response.status_code != 200:
            log_parser.logger.error(
                "Request to slack returned an error %s, the response is:\n%s"
                % (response.status_code, response.text)
            )
        else:
            log_parser.logger.info("Posted to slack")


if __name__ == "__main__":
    main()

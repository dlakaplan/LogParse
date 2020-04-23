#!/usr/bin/env python
from __future__ import print_function, division
import argparse
import glob
import os
import datetime
import re
import logging
import sys

from cima_log_parser import log_parser


def main():
    programs=['p2945','p2780']
    
    parser = argparse.ArgumentParser(description='Parse an Arecibo CIMA log file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--file', '-f',
                        type=str,
                        nargs='+',
                        default=None,
                        help='Name(s) of CIMA log file(s)')
    parser.add_argument('--directory', '-d',
                        type=str,
                        default='./',
                        help='Directory to search for log files')
    parser.add_argument('--programs', '-p',
                        type=str,
                        nargs='+',
                        default=programs,
                        help='Observing programs to look for')
    parser.add_argument('--days', '-t',
                        type=int,
                        default=1,
                        help='Days in the past to look for log files (<=0: find all)')
    parser.add_argument('--tolerance',
                        type=int,
                        default=100,
                        help='Tolerance for printing out exposure difference marks')
    parser.add_argument('--email', '-e',
                        type=str,
                        default=None,
                        help='Send email with results')
    parser.add_argument('--out', '-o',
                        default='stdout',
                        type=str,
                        help='Output destination')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increase verbosity')                   
    
    args = parser.parse_args()
    if args.verbose == 0:
        log_parser.logger.setLevel(logging.WARNING)
    elif args.verbose == 1:
        log_parser.logger.setLevel(logging.INFO)
    elif args.verbose == 2:
        log_parser.logger.setLevel(logging.DEBUG)

    if args.out == 'stdout':
        args.out = sys.stdout
    else:
        args.out = open(args.out, 'w')
        # add in a second logger that outputs to the same file as the main output destination
        newhandler = logging.StreamHandler(args.out)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        newhandler.setFormatter(formatter)
        log_parser.logger.addHandler(newhandler)


    if args.file is None:
        files=[]
        for program in args.programs:
            files+=sorted(glob.glob(os.path.join(args.directory,
                                                 '{}.cimalog_*'.format(program))))
        if args.days>0:
            today=datetime.date.today()
            good_files=[]
            for file in files:
                match = re.match(
                    r".*?.cimalog_(?P<datetime>\d{4}\d{2}\d{2})",
                    file,
                    )
                if match:
                    _datetime = datetime.datetime.strptime(match.group("datetime"), '%Y%m%d')
                    if today - _datetime.date() < datetime.timedelta(days=args.days):
                        good_files.append(file)    
        else:
            good_files=files

        if len(good_files)==0:
            log_parser.logger.error('No files found')

    else:
        good_files=args.file


    for file in good_files:
        start_line = 0
        logs=[]
        while True:
            log = log_parser.CIMAPulsarObservationLog.parse_cima_logfile(file,
                                                                         start_line = start_line,
                                                                         tolerance=args.tolerance,
                                                                         )
            if log.start_time is None:
                break
            start_line = log.end_line + 1
            logs.append(log)
            

        for log in logs:            
            log.print_results(output = args.out)
    
if __name__ == "__main__":
    main()

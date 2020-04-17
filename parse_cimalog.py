#!/usr/bin/env python
from __future__ import print_function, division
import argparse
import glob
import os
import datetime
import re
import logging
import sys

import log_parser


def main():
    programs=['p2945','p2780']
    
    parser = argparse.ArgumentParser(description='Parse an Arecibo CIMA log file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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
        #log_parser.logger.addHandler(logging.StreamHandler(sys.stdout))        
    else:
        args.out = open(args.out, 'w')
        newhandler = logging.StreamHandler(args.out)
        formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
        newhandler.setFormatter(formatter)
        log_parser.logger.addHandler(newhandler)


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
        logger.error('No files found')

    for file in good_files:
        log = log_parser.CIMAPulsarObservationLog.parse_cima_logfile(file)
        log.print_results(output = args.out)
    
if __name__ == "__main__":
    main()

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
    
    parser = argparse.ArgumentParser(description='Parse an Arecibo PUPPI command file',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file',
                        type=str,
                        nargs='+',
                        default=None,
                        help='Name(s) of PUPPI command file(s)')
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

    for file in args.file:
        cmd = log_parser.CIMAPulsarObservationPlans.parse_cima_cmdfile(file)
        cmd.print_results(output = args.out)
    
if __name__ == "__main__":
    main()

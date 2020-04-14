from __future__ import print_function

import re
import logging
import datetime
import sys
import json
from collections import OrderedDict

# create logger with 'log_parser'
logger = logging.getLogger('log_parser')
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)



class Commanded_Scan():
    """
    class for a single PUPPI scan command

    usage:
    c=Commanded_Scan(<log lines>)

    an entry is like:

    LOAD cima_control_puppi_1410.conf
    EXEC vw_send "pnt wrap -1"
    SEEK J1640+2224
    EXEC vw_send "pnt wrap 0"
    EXEC change_puppi_parfile "/home/gpu/tzpar/1640+2224.par"
    EXEC change_puppi_dumptime "FOLD" "10" "2048"
    EXEC change_puppi_dumptime "CAL" "10" "2048"
    ADJUSTPOWER
    #EXEC wait_puppi_temporary "180" "Check PUPPI power levels"
    SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
    PULSARON

    it begins with "LOAD" and ends with "PULSARON"
    if the block is ended without "PULSARON", then it is assumed that the command is not executed ('execute'=False)

    the settings are stored in the dictionary c._data
    which can be dumped to json as c.asjson()
        
    Based on the specs at:
    http://www.naic.edu/~cima/cima_puppi.html
    """

    def __init__(self, loglines):
        self._data=OrderedDict({'execute': False})

        if not loglines[0].startswith('LOAD'):
            logging.error('Commanded scan did not start with LOAD')
            return None
        for line in loglines:
            if line.startswith('#'):
                # ignore comments
                continue
            if line.startswith('LOAD'):
                try:
                    m=re.match(r"cima_control_puppi_(\d+).conf",
                               line.split()[-1])
                    if m:
                        self._data['frequency'] = int(m.groups()[0])                        
                    logging.debug('Frequency = {}'.format(self._data['frequency']))
                except ValueError:
                    logging.error('Unable to parse frequency from line:\n.{}'.format(line))
                    return None
            elif line.startswith('SEEK'):
                self._data['target'] = line.split()[-1]
                logging.debug('Target = {}'.format(self._data['target']))

            elif line.startswith('EXEC'):
                if 'change_puppi_parfile' in line:
                    self._data['parfile'] = line.split()[-1].replace('"','')
                elif 'change_puppi_dumptime' in line:
                    if 'FOLD' in line:
                        self._data['fold_dumptime'],self._data['fold_bins'] = map(int, line.replace('"','').split()[-2:])
                    elif 'CAL' in line:
                        self._data['cal_dumptime'],self._data['cal_bins'] = map(int, line.replace('"','').split()[-2:])
            elif line.startswith('SETUP'):
                if 'pulsaron' in line:
                    # remainder is key=value pairs
                    # first be careful that the spacing may be inconsistent
                    # allow for key=value, key = value, etc
                    line=re.sub(r"\s*=\s*",r"=",
                                line)
                    for item in line.split()[2:]:
                        key,value=item.split('=')
                        try:
                            value=int(value)
                        except ValueError:
                            pass
                        self._data[key]=value
            elif line.startswith('PULSARON'):
                self._data['execute']=True

    def __getitem__(self, key):
        """
        allow data to be accessed through the class instance
        """
        return self._data[key]

    def __str__(self):
        return "Observe PSR {} for {}s at {}MHz".format(self._data['target'],
                                                        self._data['secs'],
                                                        self._data['frequency'])
    def __repr__(self):
        return str(self)

    def asjson(self):
        return json.dumps(self._data)

class Command_Parser():
    """
    class to parse a whole PUPPI command file

    usage:
    c=Command_Parser(<log file>)

    it separates the file into blocks that start with "LOAD"
    each block is sent to Commanded_Scan() for parsing
    the results are saved as a list of commands, self.commands

    can be output to a dictionary:
    c.asdict()
    or JSON:
    c.asjson()    

    """


    def __init__(self, filename):

        self.commands=[]
        self.catalog=None
        self.total_time=0
        
        with open(filename) as f:
            self.filename=filename
            lines=f.readlines()

        logging.debug('Reading {0}'.format(self.filename))

        ending_number = None
        finished_command = True
        for i,line in enumerate(lines):
            if line.startswith('#'):
                continue
            if line.startswith('catalog'):
                self.catalog=line.split()[-1]

            if line.startswith('LOAD'):
                if ending_number is None and not finished_command:
                    # we didn't close the previous command
                    self.load_command(lines[starting_number:i+1])
                
                starting_number=i
                ending_number=None
                finished_command=False
                
            elif line.startswith('PULSARON'):
                ending_number=i+1
                finished_command=True
        
            if finished_command and ending_number is not None:
                self.load_command(lines[starting_number:ending_number])
                ending_number=None
        

    def load_command(self, lines):
        self.commands.append(Commanded_Scan(lines))
        logging.info(str(self.commands[-1]))
        if not self.commands[-1]._data['execute']:
            logging.warning('Scan is not executed')
        else:
            self.total_time+=self.commands[-1]._data['secs']

    def asdict(self):
        data=OrderedDict()
        data['filename']=self.filename
        data['catalog']=self.catalog,
        data['total_time']=self.total_time
        data['commands']=[]
        for c in self.commands:
            data['commands'].append(c._data)
        return data

    def asjson(self):
        return json.dumps(self.asdict())

    def __repr__(self):
        s='PUPPI commands from {}, using catalog {}, total time to execute: {}s\n'.format(self.filename,
                                                                                          self.catalog,
                                                                                          self.total_time)
        return s
    
    def __str__(self):
        s=['PUPPI commands from {}, using catalog {}, total time to execute: {}s'.format(self.filename,
                                                                                         self.catalog,
                                                                                         self.total_time)]
        for c in self.commands:
            s.append(str(c))
        return '\n'.join(s)




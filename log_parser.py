from __future__ import print_function

import re
import logging
import datetime
import sys
import json
from collections import OrderedDict
import os

# create logger with 'log_parser'
logging.basicConfig()
logger = logging.getLogger('log_parser')
logger.setLevel(logging.INFO)


##################################################
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

    def __init__(self, loglines, start=0, command_type="request"):
        self._data=OrderedDict({'execute': False})
        self._data['start_linenumber']=-1
        self._data['end_linenumber']=-1

        self.command_type=command_type
        
        if not loglines[0].startswith('LOAD'):
            logger.error('Commanded scan did not start with LOAD')
            return None
        for i,line in enumerate(loglines):
            if line.startswith('#'):
                # ignore comments
                continue
            if line.startswith('LOAD'):
                self._data['start_linenumber']=start+i
                try:
                    m=re.match(r"cima_control_puppi_(\d+).conf",
                               line.split()[-1])
                    if m:
                        self._data['frequency'] = int(m.groups()[0])                        
                    logger.debug('Frequency = {}'.format(self._data['frequency']))
                except ValueError:
                    logger.error('Unable to parse frequency from line:\n.{}'.format(line))
                    return None
            elif line.startswith('SEEK'):
                self._data['target'] = line.split()[-1]
                logger.debug('Target = {}'.format(self._data['target']))

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

        self._data['end_linenumber']=start + len(loglines)

    def __getitem__(self, key):
        """
        allow data to be accessed through the class instance
        """
        return self._data[key]

    def __str__(self):
        try:
            if self._data.has_key('elapsed_time'):
                t=self._data['elapsed_time']
            else:
                t=self._data['secs']

            return "{} PSR {:<10} for {:>4}s at {:>4}MHz at linenumber {:>5} - {:>5}".format(self.command_type,
                                                                                             self._data['target'],
                                                                                             t,
                                                                                             self._data['frequency'],
                                                                                             self._data['start_linenumber'],
                                                                                             self._data['end_linenumber'])
        except KeyError:
            # some of those aren't present
            return "Bad command at linenumber {}-{}".format(self._data['start_linenumber'],
                                                            self._data['end_linenumber'])
    def __repr__(self):
        return str(self)

    def asjson(self):
        return json.dumps(self._data)

##################################################
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


    def __init__(self, filename, command_type='Request'):

        self.command_type=command_type
        self.commands=[]
        self.catalog=None
        self.total_time=0
        
        with open(filename) as f:
            self.filename=filename
            lines=f.readlines()

        logger.debug('Reading {0}'.format(self.filename))

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
                    self.load_command(lines[starting_number:i-1],
                                      starting_number)                
                starting_number=i
                ending_number=None
                finished_command=False
                
            elif line.startswith('PULSARON'):
                ending_number=i+1
                finished_command=True
        
            if finished_command and ending_number is not None:
                # process a completed command
                # LOAD -> PULSARON
                self.load_command(lines[starting_number:ending_number],
                                  starting_number)
                ending_number=None
        

    def load_command(self, lines, start=0):
        self.commands.append(Commanded_Scan(lines, start=start, command_type=self.command_type))
        logger.info(str(self.commands[-1]))
        if not self.commands[-1]._data['execute']:
            logger.warning('Scan is not executed')
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


##################################################
def parse_line(line, fmt='%Y-%b-%d %X'):
    """
    t,level,message = parse_line(<line>)
    parses the lines like:
    2020-Feb-14 07:23:37 LOG4    got_cormsg: From DATATAKING: connected    : prgMgr@dap2

    returns datetime object, level, message
    """
    
    d=line.split()
    t=datetime.datetime.strptime(d[0] + ' ' + d[1], fmt)
    level=d[2]
    return t,level,' '.join(d[3:])

def format_time(t, fmt='%Y-%b-%dT%X'):
    return datetime.datetime.strftime(t, fmt)

##################################################
class Log_Parser():
    """
    Parse a full CIMA log file

    Go through, find some basic info out (program, observer, starting time)
    find the command list and parse that for the requested commands
    then go through all of the executed commands and figure out what was actually done

    needs a lot more in the way of error handling: it isn't smart at all about parsing errors/alerts from the telescope
    or figuring out weird conditions that would stop scans

    """

    # tolerance for noting a discrepancy between the requested and executed exposure time (in s)
    # if the |difference| < tolerance, don't do anything special
    tolerance = 200

    
    def __init__(self, filename):

        self.data=OrderedDict()
        self.executed_commands=[]

        with open(filename) as f:
            self.lines=f.readlines()
        self.data['filename']=filename

        logger.debug('Reading {0}'.format(filename))

        commands=None
        last_command=None
        self.data['total_time']=0
        self.data['start_time']=None
        for i,line in enumerate(self.lines):
            t,level,message = parse_line(line)
            d=message.strip().split()                

            # we want the first instance of BEGIN
            # to set the starting time for the observing block
            # CHECK that this is desired
            if level=='BEGIN' and 'CIMA executive starting' in message:
                if self.data['start_time'] is None:
                    self.data['start_time']=t

            # collect the basic info for the log
            # CHECK about other info
            if 'CIMA session for project' in message:
                self.data['project']=d[5].replace("'","")
                self.data['mode']=d[7].replace("'","")
                self.data['operator']=' '.join(d[10:]).replace("'","")
                if self.data['mode'] != 'pulsar':
                    logger.warning('Mode is "{}", not "pulsar"'.format(self.data['mode']))
                logger.info('CIMA session for {} with operator {} started at {}'.format(self.data['project'],
                                                                                        self.data['operator'],
                                                                                        format_time(t)))

            # where were the data written
            # CHECK that this is correct
            if ('To DATATAKING' in line) and ('cd' in line):
                self.data['destination']=d[-1]
                logger.info('Data written to {}'.format(self.data['destination']))

            # read and parse the command file
            # right now what we do if we can't open the file isn't clear
            # note that these are command_type='Request'
            # also note that this can happen multiple times: only the last one is stored
            # CHECK that this behavior is correct
            if 'CIMA-load_command_file: Loaded command file' in line:
                self.data['command_file']=d[-1].replace("'","")
                if os.path.exists(self.data['command_file']):
                    self.requested_commands=Command_Parser(self.data['command_file'],
                                                           command_type='Request')
                    self.data['requested_commands']=self.requested_commands.asdict()
                else:
                    logger.error('Command file "{}" does not exist'.format(self.data['command_file']))

            # go through all of the commands
            # here we can see the commands from the session file as they are actually
            # sent to the telescope
            # CHECK:
            # are these the right levels to deal with?
            if (level in ['COMMAND', 'ALERT', 'ERROR']):

                # if the last command we issued was PULSARON
                # the next command ends the observation
                # so figure out the elapsed time
                # CHECK: are there other conditions that could end an observation?
                if last_command is not None and 'PULSARON' in last_command:
                    # this writes extra info (times)
                    # to thhe last executed commaand
                    self.executed_commands[-1]._data['end_time']=t
                    self.executed_commands[-1]._data['elapsed_time']=(self.executed_commands[-1]._data['end_time'] -
                                                                      self.executed_commands[-1]._data['start_time']).seconds
                    logger.info('Ended at {}'.format(format_time(self.executed_commands[-1]._data['end_time'])))
                    logger.info('Elapsed time is {}s'.format(
                        (self.executed_commands[-1]._data['elapsed_time'])))
                    # increment the total observing time
                    self.data['total_time']+=self.executed_commands[-1]._data['elapsed_time']
                    # reset the counter
                    last_command=None
                    

                if ('run_command_line: EXECUTING command' in line):
                    # it's running a line from the command file
                    # we can use the line number to match it up later
                    orig_linenumber=int(d[3].replace(':',''))
                    command=' '.join(d[4:]).replace("'","")
                
                    # this is the start of a pulsar observing block
                    if 'LOAD' in command:
                        # don't care if we didn't close the previous command
                        start_line=i
                        commands=[command]
                    
                    # this actually starts the observing
                    elif 'PULSARON' in command:                    
                        last_command=command
                        commands.append(command)
                        # use the same method to parse the executed commands
                        # as the requested commands, but change the command_type
                        self.executed_commands.append(Commanded_Scan(commands, start=start_line,
                                                                     command_type='Execute'))
                        logger.info(str(self.executed_commands[-1]))
                        # add in extra info: line number and start time
                        self.executed_commands[-1]._data['orig_linenumber']=orig_linenumber
                        self.executed_commands[-1]._data['start_time']=t
                        logger.info('Actually started at {}'.format(format_time(self.executed_commands[-1]._data['start_time'])))
                        # reset this once we haave parsed something
                        commands=None
                    else:
                        if commands is not None:
                            commands.append(command)
                    
        # determine these at the end
        self.data['end_time']=self.executed_commands[-1]['end_time']
        self.data['elapsed_time']=(self.data['end_time']-self.data['start_time']).seconds

        
    def __str__(self):

        s=['### NANOGrav {} observation ({:.1f}h elapsed; {:.1f}h observing; {} scans)'.format(self.data['project'],
                                                                                               self.data['elapsed_time']/3600.,
                                                                                               self.data['total_time']/3600.,
                                                                                               len(self.executed_commands))]
        s.append('### {} - {}'.format(format_time(self.data['start_time']),
                                      format_time(self.data['end_time'])))
        previous_time=self.data['start_time']
        for c in self.executed_commands:
            time_gap=(c['start_time']-previous_time).seconds
            previous_time=c['end_time']
            # we need to match it up against the request
            request=None
            for r in self.requested_commands.commands:
                if c['orig_linenumber'] == r['end_linenumber']:
                    request=r
                    break                
            if request is None:
                logger.error('Could not find a requested scan for {}'.format(c))
            else:
                note=''
                if c['elapsed_time'] - request['secs'] > self.tolerance:
                    note='***'
                if c['elapsed_time'] - request['secs'] < -self.tolerance:
                    note='---'
                s.append('{:.>6} sec --> {} ({} sec requested) {}'.format(
                    time_gap,
                    c,
                    request['secs'],
                    note))
            
        return '\n'.join(s)
            
if __name__ == "__main__":
    # for testing
    #c=Command_Parser('sessionB.cmd')
    #print(c)
    #c=Command_Parser('sessionC_No-S.cmd')
    #print(c)
    #c=Log_Parser('p2780.cimalog_20200222')
    c=Log_Parser('p2780.cimalog_20200214')

    print(c)

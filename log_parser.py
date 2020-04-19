from __future__ import print_function, division

import re
import logging
import datetime
import sys
import os
from collections import namedtuple

# create logger with 'log_parser'
logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("log_parser")
logger.setLevel(logging.INFO)

CIMALogEntry = namedtuple("CIMALogEntry", ["datetime", "levelname", "name", "message"])


def parse_log_line(line, datetime_format="%Y-%b-%d %X"):
    """
    CIMALogEntry = parse_log_line(line)

    Arguments:
        line: str - CIMA log line

    Example:
        2020-Feb-14 07:23:37 LOG4    got_cormsg: From DATATAKING: connected    : prgMgr@dap2

    CIMALogEntry contains (in this example):
    datetime = 2020-Feb-14 07:23:37
    levelname = LOG4
    name = got_cormsg
    message = From DATATAKING: connected    : prgMgr@dap2
    """
    match = re.match(
        r"^(?P<datetime>\d{4}-\w{3}-\d{2} \d{2}:\d{2}:\d{2})\s+(?P<levelname>\w+)\s+(?P<name>.+?):\s+(?P<message>.*)$",
        line,
    )
    if match:
        _datetime = datetime.datetime.strptime(match.group("datetime"), datetime_format)
        return CIMALogEntry(
            datetime=_datetime,
            levelname=match.group("levelname"),
            name=match.group("name"),
            message=match.group("message"),
        )
    else:
        logger.error("Log entry parsing failed for line %s", line)
        return None


def parse_store_command_file_line(log_message):
    """
    command_parts = parse_store_command_file_line(<line>)

    Arguments:
        log_message: str - CIMA log message

    Example message:
        From OBSERVER: store_command_file_line 32 47 {EXEC change_puppi_dumptime "CAL" "10" "2048"}

    command_parts contains (in this example):
    command_line_num = 32
    executive_line_num = 47
    command = EXEC change_puppi_dumptime "CAL" "10" "2048"    
    """
    match = re.match(
        r"^From OBSERVER: store_command_file_line (?P<command_line_num>\d+) (?P<executive_line_num>\d+) {(?P<command>.+)}$",
        log_message,
    )
    if match:
        return match.groups()
    else:
        return None


class CIMAPulsarObservationRequest(object):
    def __init__(self):
        self.source = None
        self.frequency = None
        self.duration = None
        self.setup_command_line_number = None
        self.setup_executive_line_number = None
        self.pulsaron_command_line_number = None
        self.pulsaron_executive_line_number = None
        self.parfile = None

    @property
    def executed(self):
        return self.pulsaron_command_line_number is not None

    @property
    def source_matches(self):
        return (
            os.path.splitext(os.path.basename(self.parfile))[0].replace(".par", "")
            == self.source[1:]
        )

    @property
    def parses(self):
        return self.executed and self.source_matches


class CIMAPulsarObservationExecution(object):
    def __init__(self):
        self.request = None
        self.start_time = None
        self.end_time = None
        self.logfile_start_line = None
        self.logfile_end_line = None
        self.type = 'std'

    @property
    def duration(self):
        return self.end_time - self.start_time


class CIMATrackingExecution(object):
    def __init__(self):
        self.source = None
        self.start_time = None
        self.end_time = None
        self.logfile_start_line = None
        self.logfile_end_line = None
        self.status = None


class CIMAPulsarScan(object):
    def __init__(self):
        self.request = None
        self.execution = None

    @property
    def executed_duration(self):
        return self.execution.end_time - self.execution.start_time

    @property
    def requested_duration(self):
        return self.request.duration

    @property
    def frequency(self):
        return self.request.frequency

    @property
    def source(self):
        return self.request.source

    @property
    def logfile_start_line(self):
        return self.execution.logfile_start_line

    @property
    def logfile_end_line(self):
        return self.execution.logfile_end_line

    def __str__(self):
        return "Execute PSR {:<10} ({}) for {:>4}s at {:>4}MHz at linenumber {:>5}".format(
            self.source,
            self.execution.type[:3],
            int(self.executed_duration.total_seconds()),
            self.frequency,
            self.logfile_end_line,
        )


class CIMAPulsarObservationLog(object):
    def __init__(self, tolerance=100):
        self._start_time = None
        self._end_time = None
        self._project = None
        self._mode = None
        self._operator = None
        self._data_destination = None
        self._command_file = None
        self.requested_commands = {}
        self.executed_commands = {}
        self._scans = []
        # self.tolerance = datetime.timedelta(seconds=tolerance)
        self.tolerance = tolerance
        self._filename = None

    def process_commands(self):
        for exec_line_num, request in self.requested_commands.items():
            if exec_line_num not in self.executed_commands:
                logger.warning(
                    "Requested scan of %s for %d sec at %d MHz was not executed.",
                    request.source,
                    request.duration.total_seconds(),
                    request.frequency,
                )
            else:
                execution = self.executed_commands[exec_line_num]
                scan = CIMAPulsarScan()
                scan.request = request
                scan.execution = execution
                self._scans.append(scan)
        # TODO warn if any properties are still None

    def print_results(self, output=sys.stdout):
        print(
            "### Report for: {}".format(self._filename,), file=output,
        )

        print(
            "### NANOGrav {} observation ({:.1f}h elapsed; {:.1f}h observing; {} scans)".format(
                self.project,
                self.elapsed_time.total_seconds() / 3600,
                self.observing_time.total_seconds() / 3600,
                len(self.executed_commands),
            ),
            file=output,
        )

        print("### {} - {}".format(self.start_time, self.end_time), file=output)
        self._scans.sort(key=lambda x: x.execution.start_time)
        for scan_prev, scan_current in zip([None] + self._scans, self._scans):
            if scan_prev is None:
                time_gap = scan_current.execution.start_time - self._start_time
            else:
                time_gap = (
                    scan_current.execution.start_time - scan_prev.execution.end_time
                )

            if scan_current.executed_duration < scan_current.requested_duration:

                note = ["-"] * int(
                    (
                        scan_current.requested_duration - scan_current.executed_duration
                    ).total_seconds()
                    / float(self.tolerance)
                )
                note = "".join(note)
            else:
                note = ["+"] * int(
                    (
                        scan_current.executed_duration - scan_current.requested_duration
                    ).total_seconds()
                    / float(self.tolerance)
                )
                note = "".join(note)

            print(
                "{:>6} sec --> {} ({} sec requested) {}".format(
                    time_gap.total_seconds(),
                    scan_current,
                    scan_current.requested_duration.total_seconds(),
                    note,
                ),
                file=output,
            )

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        if self._start_time is not None:
            logger.warning(
                "Existing observation log start time overwritten! From %s to %s.",
                self._start_time,
                value,
            )
        self._start_time = value

    @property
    def end_time(self):
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        if self._end_time is not None:
            logger.warning(
                "Existing observation log end time overwritten! From %s to %s.",
                self._end_time,
                value,
            )
        self._end_time = value

    @property
    def elapsed_time(self):
        return self.end_time - self.start_time

    @property
    def observing_time(self):
        return sum(
            [scan.executed_duration for scan in self._scans], datetime.timedelta()
        )

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        if self._project is not None:
            logger.warning(
                "Existing observation project overwritten! From %s to %s.",
                self._project,
                value,
            )
        self._project = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        if self._mode is not None:
            logger.warning(
                "Existing observation mode overwritten! From %s to %s.",
                self._mode,
                value,
            )
        if value != "pulsar":
            logger.warning("Mode is %s, not 'pulsar'.", value)
        self._mode = value

    @property
    def operator(self):
        return self._operator

    @operator.setter
    def operator(self, value):
        if self._operator is not None:
            logger.warning(
                "Existing observation operator overwritten! From %s to %s.",
                self._operator,
                value,
            )
        self._operator = value

    @property
    def data_destination(self):
        return self._data_destination

    @data_destination.setter
    def data_destination(self, value):
        if self._data_destination is not None:
            logger.warning(
                "Existing observation data destination overwritten! From %s to %s.",
                self._data_destination,
                value,
            )
        self._data_destination = value

    @property
    def command_file(self):
        return self._command_file

    @command_file.setter
    def command_file(self, value):
        if self._command_file is not None:
            logger.warning(
                "Existing observation command file overwritten! From %s to %s.",
                self._command_file,
                value,
            )
        self._command_file = value

    @staticmethod
    def parse_cima_logfile(filename, tolerance=100):
        """
            Parse a full CIMA log file.

        Go through, find some basic info out (program, observer, starting time)
        find the command list and parse that for the requested commands
            then go through all of the executed commands and figure out what was actually done.

            Arguments:
                filename: str - filename of the log file.
            Keyword arguments:
                tolerance: int - if an executed scan duration exceeds the requested duration
                    minus the tolerance (in seconds), mark the scan.
        """

        # tolerance for noting a discrepancy between the requested and executed exposure time (in s)
        # if the |difference| < tolerance, don't do anything special

        logger.info("Looking at {} ...".format(filename))
        log = CIMAPulsarObservationLog(tolerance=tolerance)
        log._filename = filename
        parsing_stored_commands = False
        f = open(filename)
        line_iterator = f.__iter__()
        line_num = 0
        tracking = None
        for line in line_iterator:
            log_entry = parse_log_line(line.strip())
            if log_entry is None:
                continue
            # start of observation block
            if log_entry.name == "executive" and log_entry.levelname == "BEGIN":
                log.start_time = log_entry.datetime
            # collect the basic info for the log
            elif (
                log_entry.name == "executive"
                and log_entry.levelname == "INFO1"
                and "CIMA session for project" in log_entry.message
            ):
                tokens = log_entry.message.split("'")
                log.project = tokens[1]
                log.mode = tokens[3]
                log.operator = tokens[5]
                logger.info(
                    "CIMA session for %s with operator %s started at %s",
                    log.project,
                    log.operator,
                    log_entry.datetime,
                )
            # where were the data written
            elif (
                log_entry.levelname == "LOG4"
                and log_entry.name == "vw_send"
                and "To DATATAKING: cd" in log_entry.message
            ):
                log.data_destination = log_entry.message.split()[-1]
                logger.info("Data written to %s", log.data_destination)
            # name of the input command file
            elif (
                log_entry.levelname == "INFO4"
                and log_entry.name == "CIMA-load_command_file"
            ):
                log.command_file = log_entry.message.split("'")[-2]
            # first command line storage command
            elif (
                log_entry.levelname == "LOG4"
                and log_entry.name == "exec_msg"
                and "store_command_file_line" in log_entry.message
            ):
                # TODO warn user if stored commands are found more than once
                parsing_stored_commands = True
                # continue to parse lines to capture all command line inputs
                while parsing_stored_commands:
                    command_parts = parse_store_command_file_line(log_entry.message)
                    if command_parts is not None:
                        cmd_line_num, exec_line_num, cmd = command_parts
                        if "LOAD" in cmd:
                            # this command starts a new observing block
                            conf_file = cmd.split()[-1]
                            freq_mhz = int(
                                conf_file.replace(".conf", "").split("_")[-1]
                            )
                            # create a new blank CIMAPulsarObservationRequest object
                            request = CIMAPulsarObservationRequest()
                            request.frequency = freq_mhz
                        elif "SEEK" in cmd:
                            # this identifies the source name
                            request.source = cmd.split()[-1]
                        elif "SETUP pulsaron" in cmd:
                            # sets various parameters
                            # given by key=value pairs
                            request.setup_command_line_number = int(cmd_line_num)
                            request.setup_executive_line_number = int(exec_line_num)
                            d = {}
                            for kv in cmd.split()[2:]:
                                k, v = kv.split("=")
                                d[k] = v
                            request.duration = datetime.timedelta(
                                seconds=int(d["secs"])
                            )
                        elif cmd.startswith("EXEC") and "change_puppi_parfile" in cmd:
                            request.parfile = cmd.split()[-1].replace('"', "")
                        elif "PULSARON" in cmd:
                            # this terminates an observing block.
                            # if not present the pulsaron_command_line_number
                            # and pulsaron_executive_line_number are not set
                            # so we know that it won't be executed
                            request.pulsaron_command_line_number = int(cmd_line_num)
                            request.pulsaron_executive_line_number = int(exec_line_num)
                            log.requested_commands[
                                request.pulsaron_executive_line_number
                            ] = request
                        elif "EXEC ponoffcal" in cmd:
                            # also terminate a pulsar observing block
                            # for calibration
                            request.pulsaron_command_line_number = int(cmd_line_num)
                            request.pulsaron_executive_line_number = int(exec_line_num)
                            match = re.match(r'EXEC ponoffcal "(\d+)".*',
                                             cmd)
                            if match:
                                request.duration = datetime.timedelta(
                                    seconds=int(match.groups()[0]),
                                    )
                            log.requested_commands[
                                request.pulsaron_executive_line_number
                            ] = request
                        log_entry = parse_log_line(next(line_iterator).strip())
                        line_num += 1
                    else:
                        # stop parsing stored commands
                        parsing_stored_commands = False
            # end of observation block
            elif log_entry.levelname == "ALERT" and log_entry.name == "CIMA-exit_cima":
                log.end_time = log_entry.datetime

            # initialisation of a pulsar observation
            # no elif as execution resumes here after parsing the stored commands
            if (
                log_entry.levelname == "COMMAND"
                and log_entry.name == "run_command_line"
                and "PULSARON" in log_entry.message
            ):
                match = re.match(
                    r"^EXECUTING command (?P<executive_line_num>\d+): '(?P<command>.+?)'$",
                    log_entry.message,
                )
                if match:
                    exec_line_num = int(match.group("executive_line_num"))
                    execution = CIMAPulsarObservationExecution()
                    execution.request = log.requested_commands[exec_line_num]
                    execution.logfile_start_line = line_num
                else:
                    logger.error(
                        "Failed to parse run_command_line for PULSARON: %s",
                        log_entry.message,
                    )

            # initialisation of a pulsar cal observation
            elif (
                log_entry.levelname == "COMMAND"
                and log_entry.name == "run_command_line"
                and "EXEC ponoffcal" in log_entry.message
            ):
                match = re.match(
                    r"^EXECUTING command (?P<executive_line_num>\d+): '(?P<command>.+?)'$",
                    log_entry.message,
                )
                if match:
                    exec_line_num = int(match.group("executive_line_num"))
                    execution = CIMAPulsarObservationExecution()
                    execution.request = log.requested_commands[exec_line_num]
                    execution.logfile_start_line = line_num
                else:
                    logger.error(
                        "Failed to parse run_command_line for PULSARON: %s",
                        log_entry.message,
                    )

            # actual start of pulsar observation
            # only occurs if another error did not prevent it from starting
            elif (
                log_entry.levelname == "BEGIN"
                and log_entry.name == "begin_task"
                and "Starting task 'pulsar on" in log_entry.message
            ):
                execution.start_time = log_entry.datetime
                execution.logfile_end_line = line_num
                log.executed_commands[exec_line_num] = execution
                if 'calibration' in log_entry.message:
                    execution.type='cal'
                logger.info("Starting pulsar observation (%s) at %s line = %d",
                            execution.type,
                            log_entry.datetime,
                            line_num)
            # end of pulsar observation
            elif (
                log_entry.levelname == "END"
                and log_entry.name == "end_task"
                and "pulsar on" in log_entry.message
            ):
                execution.end_time = log_entry.datetime
                logger.info("Ending pulsar observation at %s line = %d", log_entry.datetime, line_num)

            # start a new tracking task
            elif log_entry.levelname == "BEGIN" and log_entry.name == "begin_task":
                match = re.match(
                    r"Starting task 'tracking source '(.*?)''", log_entry.message,
                )
                if match:
                    tracking = CIMATrackingExecution()
                    tracking.logfile_start_line = line_num
                    tracking.start_time = log_entry.datetime
                    tracking.source = match.groups()[0]
                    logger.info(
                        "Starting to track PSR %s at %s",
                        tracking.source,
                        tracking.start_time,
                    )
            # abort part-way through
            elif (
                log_entry.levelname == "LOG4"
                and log_entry.name == "exec_msg"
                and "abort_task skip" in log_entry.message
            ):
                if tracking is not None:
                    logger.warning(
                        "Aborting current scan on target PSR %s at %s at line %d (started at %s; tracking duration %ds)",
                        tracking.source,
                        log_entry.datetime,
                        line_num,
                        tracking.start_time,
                        (log_entry.datetime - tracking.start_time).total_seconds(),
                    )
            # end tracking in good standing
            elif log_entry.levelname == "END" and log_entry.name == "end_task":
                match = re.match(
                    "Finishing task 'tracking source '(?P<source>.*?)'' with status '(?P<status>.*?)'",
                    log_entry.message,
                )
                if match:
                    tracking.end_time = log_entry.datetime
                    tracking.logfile_end_line = line_num
                    if match.group("status") == "OK":
                        logger.info(
                            "Ending tracking of %s at %s with status %s",
                            match.group("source"),
                            log_entry.datetime,
                            match.group("status"),
                        )
                    else:
                        logger.warning(
                            "Ending tracking of %s at %s with status %s",
                            match.group("source"),
                            log_entry.datetime,
                            match.group("status"),
                        )

            line_num += 1
        f.close()
        log.process_commands()
        return log


class CIMAPulsarObservationPlans(object):
    def __init__(self):
        self.requested_commands = []

    @staticmethod
    def parse_cima_cmdfile(filename):
        commands = CIMAPulsarObservationPlans()

        f = open(filename)
        for line_number, cmd in enumerate(f):
            if cmd.startswith("#"):
                continue
            if cmd.startswith("LOAD"):
                # this command starts a new observing block
                conf_file = cmd.split()[-1]
                freq_mhz = int(conf_file.replace(".conf", "").split("_")[-1])
                # create a new blank CIMAPulsarObservationRequest object
                request = CIMAPulsarObservationRequest()
                request.frequency = freq_mhz
                request.setup_command_line_number = line_number
                commands.requested_commands.append(request)
            elif cmd.startswith("SEEK"):
                # this identifies the source name
                commands.requested_commands[-1].source = cmd.split()[-1]
            elif cmd.startswith("SETUP pulsaron"):
                # sets various parameters
                # given by key=value pairs
                d = {}
                for kv in cmd.split()[2:]:
                    k, v = kv.split("=")
                    d[k] = v
                commands.requested_commands[-1].duration = datetime.timedelta(
                    seconds=int(d["secs"])
                )
            elif cmd.startswith("EXEC") and "change_puppi_parfile" in cmd:
                commands.requested_commands[-1].parfile = cmd.split()[-1].replace(
                    '"', ""
                )
            elif cmd.startswith("PULSARON"):
                # this terminates an observing block.
                # if not present the pulsaron_command_line_number
                # and pulsaron_executive_line_number are not set
                # so we know that it won't be executed
                commands.requested_commands[-1].pulsaron_command_line_number = int(
                    line_number
                )
        f.close()

        # go through the requested commands
        # and do some basic checks
        for request in commands.requested_commands:
            if not request.executed:
                logger.warning(
                    "Requested scan of %s for %d sec at %d MHz [line=%d] was not executed.",
                    request.source,
                    request.duration.total_seconds(),
                    request.frequency,
                    request.setup_command_line_number,
                )
            if not request.source_matches:
                logger.warning(
                    'Requested scan of %s for %d sec at %d MHz [line=%d]: parfile "%s" does not match source "%s"',
                    request.source,
                    request.duration.total_seconds(),
                    request.frequency,
                    request.setup_command_line_number,
                    request.parfile,
                    request.source,
                )

        return commands

    def print_results(self, output=sys.stdout):
        for request in self.requested_commands:
            note = ""
            if not request.parses:
                note = "*"
            print(
                "Request PSR {:<10} for {:>4}s at {:>4}MHz at linenumber {:>5} {}".format(
                    request.source,
                    int(request.duration.total_seconds()),
                    request.frequency,
                    request.setup_command_line_number,
                    note,
                ),
                file=output,
            )


if __name__ == "__main__":
    log = CIMAPulsarObservationLog.parse_cima_logfile("p2780.cimalog_20200214")
    log.print_results()

    # cmd = CIMAPulsarObservationPlans.parse_cima_cmdfile("sessionB.cmd")
    # cmd.print_results()

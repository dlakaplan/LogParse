from __future__ import print_function, division

import math
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

GBTLogEntry = namedtuple("LogEntry", ["datetime", "message"])

# mapping between band name and frequency
# adjust as needed
frequency_from_band = {"L": 1500, "S": 2300, "820": 820}


def parse_cima_log_line(line, datetime_format="%Y-%b-%d %X"):
    """
    CIMALogEntry = parse_cima_log_line(line)

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


def parse_cima_store_command_file_line(log_message):
    """
    command_parts = parse_cima_store_command_file_line(<line>)

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


def to_mjd(dt):
    """
    Converts a given datetime object to modified Julian date.
    Algorithm is copied from https://en.wikipedia.org/wiki/Julian_day
    All variable names are consistent with the notation on the wiki page.
    Parameters
    ----------
    fmt
    dt: datetime
        Datetime object to convert to MJD
    Returns
    -------
    mjd: float

    https://github.com/dannyzed/julian/blob/master/julian/julian.py
    """
    a = math.floor((14 - dt.month) / 12)
    y = dt.year + 4800 - a
    m = dt.month + 12 * a - 3

    jdn = (
        dt.day
        + math.floor((153 * m + 2) / 5)
        + 365 * y
        + math.floor(y / 4)
        - math.floor(y / 100)
        + math.floor(y / 400)
        - 32045
    )

    jd = (
        jdn
        + (dt.hour - 12) / 24
        + dt.minute / 1440
        + dt.second / 86400
        + dt.microsecond / 86400000000
    )
    return jd - 2400000.5


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
        self.power_check = False

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
        return self.executed and self.source_matches and not self.power_check

    def __str__(self):
        return "Observe {} at {} MHz for {}".format(
            self.source, self.frequency, self.duration,
        )


class CIMAPulsarObservationExecution(object):
    def __init__(self):
        self.request = None
        self.slewing = None
        self.start_time = None
        self.end_time = None
        self.logfile_start_line = None
        self.logfile_end_line = None
        self.type = "std"
        self.scan_numbers = []
        self.scan_cals = []
        self.winking_cal = False

    @property
    def duration(self):
        return self.end_time - self.start_time


class CIMASlewingExecution(object):
    def __init__(self):
        self.source = None
        self.start_time = None
        self.end_time = None
        self.logfile_start_line = None
        self.logfile_end_line = None
        self.status = None

    @property
    def duration(self):
        return self.end_time - self.start_time


class CIMAPulsarScan(object):
    def __init__(self):
        self.request = None
        self.execution = None

    @property
    def slew_duration(self):
        return self.execution.slewing.end_time - self.execution.slewing.start_time

    @property
    def start_time(self):
        return self.execution.start_time

    @property
    def end_time(self):
        return self.execution.end_time

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
        self._modtime = None
        self.end_line = None
        self.start_line = None

    def process_commands(self):
        for exec_line_num, request in self.requested_commands.items():
            if exec_line_num not in self.executed_commands:
                logger.warning(
                    "Requested scan of %s for %d sec at %d MHz [line=%d] was not executed.",
                    request.source,
                    request.duration.total_seconds(),
                    request.frequency,
                    request.setup_executive_line_number,
                )
            else:
                execution = self.executed_commands[exec_line_num]
                scan = CIMAPulsarScan()
                scan.request = request
                scan.execution = execution
                self._scans.append(scan)
        # TODO warn if any properties are still None

    def construct_filenames(self, scan):
        # which is the appropripate MJD to use?
        # is it the start time? end time?  Can it change for a given source?
        mjd = to_mjd(scan.start_time)
        filenames = []
        for scan_number, scan_cal in zip(
            scan.execution.scan_numbers, scan.execution.scan_cals
        ):
            filename = "puppi_{:d}_{}_{:04d}".format(
                int(mjd), scan.source, scan_number,
            )
            if scan_cal:
                filename += "_cal"
            filenames.append(filename)

        return filenames

    def print_results(self, output=sys.stdout):
        print(
            "##############################\n### Report for: {} starting at line {}".format(
                self.filename, self.start_line,
            ),
            file=output,
        )

        if self.start_time is None:
            return None

        print(
            "### NANOGrav {} observation ({:.1f}h elapsed; {:.1f}h observing; {:.1f}m slewing; {} scans)".format(
                self.project,
                self.elapsed_time.total_seconds() / 3600,
                self.observing_time.total_seconds() / 3600,
                self.slewing_time.total_seconds() / 60,
                len(self.executed_commands),
            ),
            file=output,
        )

        print("### {} - {}".format(self.start_time, self.end_time), file=output)

        if self.data_destination is None:
            logger.warning("Data destination is not set")
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
                "{:>6} sec ({:>6} sec slewing) --> {} at {} ({} sec requested) {}".format(
                    int(time_gap.total_seconds()),
                    int(scan_current.execution.slewing.duration.total_seconds()),
                    scan_current,
                    scan_current.start_time,
                    int(scan_current.requested_duration.total_seconds()),
                    note,
                ),
                file=output,
            )

            print(
                "\tWriting to {}".format(
                    ", ".join(self.construct_filenames(scan_current)),
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
    def slewing_time(self):
        return sum([scan.slewingduration for scan in self._scans], datetime.timedelta())

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
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self._modtime = datetime.datetime.fromtimestamp(
            os.path.getmtime(self._filename)
        )

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
                "Existing observation command file overwritten! From %s to %s.  Deleting %d requested observations",
                self._command_file,
                value,
                len(self.requested_commands.items()),
            )
            self.requested_commands = {}
        else:
            logger.debug(
                "Setting command file to %s.", value,
            )
        self._command_file = value

    @staticmethod
    def parse_cima_logfile(filename, start_line=0, tolerance=100):
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

        if start_line > 0:
            logger.info("##############################")
            logger.info("")
        logger.info("Looking at {} ...".format(filename))
        log = CIMAPulsarObservationLog(tolerance=tolerance)
        log.filename = filename
        parsing_stored_commands = False
        if datetime.datetime.now() - log._modtime < datetime.timedelta(seconds=60):
            logger.warning(
                "File modification time was only %d sec ago...File may still be in progress.",
                (datetime.datetime.now() - log._modtime).total_seconds(),
            )
        f = open(filename)
        line_iterator = f.__iter__()
        line_num = 0
        log.start_line = start_line
        if start_line > 0:
            logger.info(
                "Starting at line %d", start_line,
            )
        while line_num < start_line:
            next(line_iterator)
            line_num += 1
        slewing = None
        for line in line_iterator:
            log_entry = parse_cima_log_line(line.strip())
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
                "LOG" in log_entry.levelname
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
                    command_parts = parse_cima_store_command_file_line(
                        log_entry.message
                    )
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
                            logger.debug(
                                "Request: %s from line %d on line %d",
                                request,
                                int(exec_line_num),
                                line_num,
                            )

                        elif "EXEC ponoffcal" in cmd:
                            # also terminate a pulsar observing block
                            # for calibration
                            request.pulsaron_command_line_number = int(cmd_line_num)
                            request.pulsaron_executive_line_number = int(exec_line_num)
                            match = re.match(r'EXEC ponoffcal "(\d+)".*', cmd)
                            if match:
                                request.duration = datetime.timedelta(
                                    seconds=int(match.groups()[0]),
                                )
                            log.requested_commands[
                                request.pulsaron_executive_line_number
                            ] = request
                            logger.debug(
                                "Request: %s from line %d on line %d",
                                request,
                                int(exec_line_num),
                                line_num,
                            )
                        log_entry = parse_cima_log_line(next(line_iterator).strip())
                        line_num += 1
                    else:
                        # stop parsing stored commands
                        parsing_stored_commands = False
            # end of observation block
            elif log_entry.levelname == "ALERT" and log_entry.name == "CIMA-exit_cima":
                log.end_time = log_entry.datetime
                log.end_line = line_num
                logger.debug("Exiting CIMA at %s line %d", log.end_time, line_num)
                break

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
                    execution.slewing = slewing
                    execution.logfile_start_line = line_num
                    if not (slewing.source == execution.request.source):
                        logger.warning(
                            "Tracking source %s, but observation request is for source %s (line %d)",
                            slewing.source,
                            execution.request.source,
                            line_num,
                        )
                        execution
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
                        "Failed to parse run_command_line for ponoffcal: %s",
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
                if exec_line_num in log.executed_commands.keys():
                    logger.warning(
                        "Command from line %d already exists from %s; not replacing",
                        exec_line_num,
                        log.executed_commands[exec_line_num].start_time,
                    )
                else:
                    log.executed_commands[exec_line_num] = execution
                    if "calibration" in log_entry.message:
                        execution.type = "cal"
                    logger.info(
                        "Starting pulsar observation (%s) at %s line = %d",
                        execution.type,
                        log_entry.datetime,
                        line_num,
                    )
            # end of pulsar observation
            elif (
                log_entry.levelname == "END"
                and log_entry.name == "end_task"
                and "pulsar on" in log_entry.message
            ):
                execution.end_time = log_entry.datetime
                logger.info(
                    "Ending pulsar observation at %s line = %d",
                    log_entry.datetime,
                    line_num,
                )

            # pick up the scan id to get the filename
            elif (
                log_entry.levelname == "WARNING"
                and log_entry.name == "from_puppi"
                and "Coherent mode Started" in log_entry.message
            ):
                execution.scan_numbers.append(int(log_entry.message.split()[-1]))
                execution.scan_cals.append(execution.winking_cal,)
                logger.info(
                    "Adding scan number %d (cal = %s) line = %d",
                    execution.scan_numbers[-1],
                    execution.scan_cals[-1],
                    line_num,
                )

            # look for whether the winking cal is on or not (toggle)
            elif (
                log_entry.levelname == "INFO2"
                and log_entry.name == "winking_cal"
                and "25 Hz calibrator switched" in log_entry.message
            ):
                match = re.match(
                    r"25 Hz calibrator switched (?P<state>\w+)", log_entry.message,
                )
                if match:
                    if match.group("state") == "ON":
                        execution.winking_cal = True
                    else:
                        execution.winking_cal = False
                logger.debug(
                    "Winking cal = %s line = %d", execution.winking_cal, line_num,
                )

            # start a new tracking (really slewing) task
            elif log_entry.levelname == "BEGIN" and log_entry.name == "begin_task":
                match = re.match(
                    r"Starting task 'tracking source '(.*?)''", log_entry.message,
                )
                if match:
                    slewing = CIMASlewingExecution()
                    slewing.logfile_start_line = line_num
                    slewing.start_time = log_entry.datetime
                    slewing.source = match.groups()[0]
                    logger.info(
                        "Starting to track PSR %s at %s line = %d",
                        slewing.source,
                        slewing.start_time,
                        line_num,
                    )
            # abort part-way through
            elif (
                log_entry.levelname == "LOG4"
                and log_entry.name == "exec_msg"
                and "abort_task skip" in log_entry.message
            ):
                if slewing is not None:
                    logger.warning(
                        "Aborting current scan on target PSR %s at %s at line %d (started at %s; tracking duration %ds)",
                        slewing.source,
                        log_entry.datetime,
                        line_num,
                        slewing.start_time,
                        (log_entry.datetime - slewing.start_time).total_seconds(),
                    )
            # end slewing in good standing
            elif log_entry.levelname == "END" and log_entry.name == "end_task":
                match = re.match(
                    "Finishing task 'tracking source '(?P<source>.*?)'' with status '(?P<status>.*?)'",
                    log_entry.message,
                )
                if match:
                    slewing.end_time = log_entry.datetime
                    slewing.logfile_end_line = line_num
                    if match.group("status") == "OK":
                        logger.info(
                            "Ending slewing to %s at %s with status '%s' line = %d",
                            match.group("source"),
                            log_entry.datetime,
                            match.group("status"),
                            line_num,
                        )
                    else:
                        logger.warning(
                            "Ending slewing to %s at %s with status '%s' line = %d",
                            match.group("source"),
                            log_entry.datetime,
                            match.group("status"),
                            line_num,
                        )

            # various errors
            elif log_entry.levelname == "ERROR":
                # if log_entry.name == "send_puppi_obs_conf":
                logger.warning(
                    "%s at %s line = %d",
                    log_entry.message,
                    log_entry.datetime,
                    line_num,
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
            elif cmd.startswith("EXEC") and "wait_puppi_temporary" in cmd:
                logger.warning(
                    "Uncommented power check on line %d", int(line_number),
                )
                commands.requested_commands[-1].power_check = True
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


class GBTSlewingExecution(object):
    def __init__(self):
        self.source = None
        self.start_time = None
        self.end_time = None
        self.logfile_start_line = None
        self.logfile_end_line = None
        # to implement?
        self.status = None
        self.frequency = None

    @property
    def duration(self):
        return self.end_time - self.start_time


class GBTPulsarObservationRequest(object):
    def __init__(self):
        self.source = None
        self.frequency = None
        self.start_time = None
        self.end_time = None

    @property
    def duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return "Observe {} at {} MHz for {}".format(
            self.source, self.frequency, self.duration,
        )


class GBTPulsarScan(object):
    def __init__(self):
        self.slewing = None
        self.start_time = None
        self.end_time = None
        self.logfile_start_line = None
        self.logfile_end_line = None
        self.scan_number = None
        self.source = None
        self.frequency = None
        # not implemented
        self.execution_type = "std"

    @property
    def slew_duration(self):
        return self.slewing.end_time - self.slewing.start_time

    @property
    def duration(self):
        return self.end_time - self.start_time

    def __str__(self):
        return "Execute PSR {:<10} ({}) for {:>4}s at {:>4}MHz at linenumber {:>5}".format(
            self.source,
            self.execution_type[:3],
            int(self.duration.total_seconds()),
            self.frequency,
            self.logfile_end_line,
        )


class GBTPulsarObservation(object):
    def __init__(self):
        self.science_scan = None
        self.cal_scan = None

    @property
    def execution_type(self):
        return self.science_scan.execution_type

    @property
    def frequency(self):
        return self.cal_scan.frequency

    @property
    def source(self):
        return self.cal_scan.source

    @property
    def logfile_start_line(self):
        return self.cal_scan.logfile_start_line

    @property
    def logfile_end_line(self):
        return self.science_scan.logfile_end_line

    @property
    def slewing(self):
        return self.cal_scan.slewing

    @property
    def slew_duration(self):
        return self.slewing.end_time - self.slewing.start_time

    @property
    def duration(self):
        return self.end_time - self.start_time

    @property
    def cal_duration(self):
        return self.cal_scan.end_time - self.cal_scan.start_time

    @property
    def start_time(self):
        return self.science_scan.start_time

    @property
    def end_time(self):
        return self.science_scan.end_time

    @property
    def scan_numbers(self):
        return [self.cal_scan.scan_number, self.science_scan.scan_number]

    def __str__(self):
        return "Execute PSR {:<10} ({}) for {:>4}s + {:>3}s cal at {:>4}MHz at linenumber {:>5}".format(
            self.source,
            self.execution_type[:3],
            int(self.duration.total_seconds()),
            int(self.cal_duration.total_seconds()),
            self.frequency,
            self.logfile_end_line,
        )


class GBTPulsarObservationLog(object):
    def __init__(self, tolerance=100):
        self._date = None
        self._start_time = None
        self._end_time = None
        self._project = None
        self._sb_name = None
        self._mode = None
        self._operator = None
        self._observer = None
        self._scans = []
        self._filename = None
        self._modtime = None
        self.end_line = None
        self.start_line = None
        self.log_session_number = 0
        self.observing_session_number = None
        self._band = None
        self._frequency = None
        self.other_parameters = {}
        # not implemented
        self._data_destination = None
        # self.tolerance = datetime.timedelta(seconds=tolerance)
        # not used
        self.tolerance = tolerance
        # not implemented yet
        self._requests = []

    def process_commands(self):
        # match up the scans into cal/science pairs
        new_scans = []
        for i in range(0, len(self._scans), 2):
            cal_scan = self._scans[i]
            logger.debug("Identified calibration scan %s", cal_scan)
            if self._scans[i].duration.total_seconds() >= 100:
                logger.warning(
                    "Exposure time of %ds for scan %d does not make sense for a calibration scan",
                    self._scans[i].duration.total_seconds(),
                    i,
                )

            if len(self._scans) > i + 1:
                science_scan = self._scans[i + 1]
                logger.debug("Identified science scan %s", science_scan)
                if self._scans[i + 1].duration.total_seconds() < 100:
                    logger.warning(
                        "Exposure time of %ds for scan %d does not make sense for a science scan",
                        self._scans[i].duration.total_seconds(),
                        i,
                    )
            else:
                logger.warning("Cannot identify science scan to accompany scan %d", i)
                science_scan = None
            obs = GBTPulsarObservation()
            obs.cal_scan = cal_scan
            obs.science_scan = science_scan
            new_scans.append(obs)
        self._scans = new_scans

    @property
    def band(self):
        return self._band

    @band.setter
    def band(self, value):
        self._band = value
        if not value in frequency_from_band.keys():
            logger.warning(
                "Frequency for band %s not found", value,
            )
        else:
            self._frequency = frequency_from_band[value]

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
        self.observing_session_number = int(self._filename.split("_")[2])
        self._modtime = datetime.datetime.fromtimestamp(
            os.path.getmtime(self._filename)
        )

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        if self._start_time is not None:
            logger.warning(
                "Existing observation log start time is present (%s); not overwritten!",
                self._start_time,
            )
        else:
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
        return sum([scan.duration for scan in self._scans], datetime.timedelta())

    @property
    def slewing_time(self):
        return sum([scan.slew_duration for scan in self._scans], datetime.timedelta())

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
    def observer(self):
        return self._observer

    @observer.setter
    def observer(self, value):
        if self._observer is not None:
            logger.warning(
                "Existing observer overwritten! From %s to %s.", self._observer, value,
            )
        self._observer = value

    @property
    def sb_name(self):
        return self._sb_name

    @sb_name.setter
    def sb_name(self, value):
        if self._sb_name is not None:
            logger.warning(
                "Existing SB name overwritten! From %s to %s.", self._sb_name, value,
            )
        self._sb_name = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if self._date is not None:
            logger.warning(
                "Existing observation date overwritten! From %s to %s.",
                self._date,
                value,
            )
        self._date = value

    def parse_log_line(self, line, time_format="%X"):
        match = re.match(r"^\[(?P<time>\d{2}:\d{2}:\d{2})\]\s+(?P<message>.*)", line)
        if match:
            message = match.group("message")
            _datetime = datetime.datetime.strptime(match.group("time"), time_format)

            if self._date is not None:
                _datetime = datetime.datetime.combine(
                    self._date.date(), _datetime.time()
                )
                if self.start_time is not None and _datetime < self.start_time:
                    # assume it's passed a 24h boundary
                    _datetime += datetime.timedelta(days=1)

            return GBTLogEntry(
                datetime=_datetime, message=match.group("message").strip(),
            )
        else:
            return None

    @staticmethod
    def parse_gbt_logfile(filename, start_line=0, tolerance=100):

        logger.info("Looking at {} ...".format(filename))
        log = GBTPulsarObservationLog(tolerance=tolerance)
        log.filename = filename
        if datetime.datetime.now() - log._modtime < datetime.timedelta(seconds=60):
            logger.warning(
                "File modification time was only %d sec ago...File may still be in progress.",
                (datetime.datetime.now() - log._modtime).total_seconds(),
            )
        f = open(filename)
        line_iterator = f.__iter__()
        line_num = 0
        log.start_line = start_line
        if start_line > 0:
            logger.info(
                "Starting at line %d", start_line,
            )
        while line_num < start_line:
            next(line_iterator)
            line_num += 1
        slewing = None
        source = None
        last_message = None
        log_entry = None
        for line in line_iterator:
            # the stuff above here appears to be pre-amble
            # containing the astrid code etc
            # actual log starts with
            """
            #######################################################
             LOG SESSION NUMBER 1 
             """
            if log.log_session_number == 0:
                match = re.match(r"\s*LOG SESSION NUMBER (\d+)", line)
                if match:
                    log.log_session_number = int(match.groups()[0])
                    log.start_line = line_num
                    logger.info(
                        "Session %d started on line %d",
                        log.log_session_number,
                        line_num,
                    )

                # the band gets set early on in the ASTRID setup
                # it is only used in setting the band for the requests
                match = re.match(r"^band\s+=\s+'(\w+)?'", line.strip())
                if match:
                    log.band = match.groups()[0]
                    logger.info(
                        "Setting frequency to %.1f (%s band) line %s",
                        log.frequency,
                        log.band,
                        line_num,
                    )
            else:
                # if we get here, then the pre-amble is finished
                # keep track of the last line as well, since that helps interpret some things
                if log_entry is not None:
                    last_message = log_entry.message
                log_entry = log.parse_log_line(line)
                if log_entry is not None:
                    if (
                        "observer" in log_entry.message
                        and last_message == "******** Begin Scheduling Block"
                    ):
                        """
                        A line like:
                        [23:02:13] ******** observer = Zaven Arzoumanian, SB name = nanograv_timing_vegas, project ID = AGBT18B_226, date = 06 Sep 2019

                        but only after:
                        [23:02:13] ******** Begin Scheduling Block
                        """
                        entries = log_entry.message.split(",")
                        for entry in entries:
                            key, value = entry.split("=")
                            if "observer" in key.strip():
                                log.observer = value.strip()
                            elif "SB name" in key.strip():
                                log.sb_name = value.strip()
                            elif "project ID" in key.strip():
                                log.project = value.strip()
                            elif "date" in key.strip():
                                log.date = datetime.datetime.strptime(
                                    value.strip(), "%d %b %Y"
                                )
                        logger.info(
                            "Observer: %s; SB name: %s; Project: %s",
                            log.observer,
                            log.sb_name,
                            log.project,
                        )
                        log.start_time = datetime.datetime.combine(
                            log.date, log_entry.datetime.time()
                        )
                    elif log_entry.message.startswith("Src"):
                        # a planned observation
                        """
                        [23:02:13]   Src 'J1713+0747' start:2019-09-06 23:02:13.11, stop:2019-09-06 23:21:28.74
                        """
                        match = re.match(
                            r"^Src\s+'(?P<source>.*?)'\s+start:(?P<starttime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.\d{2}, stop:(?P<endtime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\.\d{2}",
                            log_entry.message,
                        )

                        if match:
                            request = GBTPulsarObservationRequest()
                            request.source = match.group("source")
                            request.start_time = datetime.datetime.strptime(
                                match.group("starttime"), "%Y-%m-%d %H:%M:%S"
                            )
                            request.end_time = datetime.datetime.strptime(
                                match.group("endtime"), "%Y-%m-%d %H:%M:%S"
                            )
                            request.frequency = log.frequency
                            log._requests.append(request)
                            logger.info(
                                "Request to %s line %d", request, line_num,
                            )

                    elif log_entry.message.startswith("source"):
                        source = log_entry.message.split(":")[1].strip()
                    elif log_entry.message == "Slewing to source.":
                        logger.info(
                            "Starting to slew to %s at %s", source, log_entry.datetime,
                        )
                        slewing = GBTSlewingExecution()
                        slewing.source = source
                        slewing.start_time = log_entry.datetime
                        slewing.logfile_start_line = line_num
                    elif "*** Notice: This subscan" in log_entry.message:
                        match = re.match(
                            r"^\*\*\* Notice: This subscan will be numbered as scan #(\d+) in your data reduction package.",
                            log_entry.message,
                        )
                        if match:
                            scan = GBTPulsarScan()
                            scan.scan_number = int(match.groups()[0])
                            scan.start_time = log_entry.datetime
                            scan.slewing = slewing
                            scan.source = source
                            scan.logfile_start_line = line_num
                            scan.frequency = float(log.other_parameters["restfreq"])
                            logger.info(
                                "Starting observation of source %s at %s",
                                source,
                                log_entry.datetime,
                            )
                    elif log_entry.message == "Setting State: Ready":
                        # see if this is the first one since slewing started
                        if slewing is not None:
                            if (
                                slewing.start_time is not None
                                and slewing.end_time is None
                            ):
                                slewing.end_time = log_entry.datetime
                                slewing.logfile_end_line = line_num
                                logger.info(
                                    "Slewing to %s ended at %s line %d",
                                    source,
                                    log_entry.datetime,
                                    line_num,
                                )

                    elif log_entry.message == "Setting State: Stopping":
                        # this is tricky, since it doesn't say what operating it's stopping
                        if scan is not None:
                            if scan.start_time is not None and scan.end_time is None:
                                scan.end_time = log_entry.datetime
                                scan.logfile_end_line = line_num
                                logger.info(
                                    "Stopping observation of source %s at %s",
                                    source,
                                    log_entry.datetime,
                                )
                                log._scans.append(scan)

                    elif log_entry.message == "******** End Scheduling Block":
                        log._end_time = log_entry.datetime
                        log.end_line = line_num

                elif "=" in line:
                    key, value = line.split("=")
                    log.other_parameters[key.strip()] = value.strip()
            line_num += 1

        f.close()
        log.process_commands()

        return log

    def print_results(self, output=sys.stdout):
        print(
            "##############################\n### Report for: {} starting at line {}".format(
                self.filename, self.start_line,
            ),
            file=output,
        )

        if self.start_time is None:
            return None

        print(
            "### NANOGrav {} observation ({:.1f}h elapsed; {:.1f}h observing; {:.1f}m slewing; {} scans)".format(
                self.project,
                self.elapsed_time.total_seconds() / 3600,
                self.observing_time.total_seconds() / 3600,
                self.slewing_time.total_seconds() / 60,
                len(self._scans),
            ),
            file=output,
        )

        print("### {} - {}".format(self.start_time, self.end_time), file=output)

        # if self.data_destination is None:
        #    logger.warning("Data destination is not set")
        self._scans.sort(key=lambda x: x.start_time)
        for scan_prev, scan_current in zip([None] + self._scans, self._scans):
            if scan_prev is None:
                time_gap = scan_current.start_time - self._start_time
            else:
                time_gap = scan_current.start_time - scan_prev.end_time

            """
            if scan_current.duration < scan_current.requested_duration:

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
                """
            note = ""

            print(
                "{:>6} sec ({:>6} sec slewing) --> {} at {} ({} sec requested) {}".format(
                    int(time_gap.total_seconds()),
                    int(scan_current.slewing.duration.total_seconds()),
                    scan_current,
                    scan_current.start_time,
                    0,
                    # int(scan_current.requested_duration.total_seconds()),
                    note,
                ),
                file=output,
            )

            """
            print(
                "\tWriting to {}".format(
                    ", ".join(self.construct_filenames(scan_current)),
                ),
                file=output,
                )
            """


if __name__ == "__main__":
    log = CIMAPulsarObservationLog.parse_cima_logfile("p2780.cimalog_20200214")
    log.print_results()

    # cmd = CIMAPulsarObservationPlans.parse_cima_cmdfile("sessionB.cmd")
    # cmd.print_results()

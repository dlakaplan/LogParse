# LogParse 

Methods to parse Arecibo PUPPI command files and CIMA logs.

## Dependencies:
All standard python, 2 (>=2.7) or 3: re, logging, datetime, sys, collections, os

## Installation:
```
pip install .
```
or
```
python ./setup.py install
```


## Command files:
```
parse_puppi -h
usage: parse_puppi [-h] [--out OUT] [--verbose] file [file ...]

Parse an Arecibo PUPPI command file

positional arguments:
  file               Name(s) of PUPPI command file(s)

optional arguments:
  -h, --help         show this help message and exit
  --out OUT, -o OUT  Output destination (default: stdout)
  --verbose, -v      Increase verbosity (default: 0)
```

```
parse_puppi examples/puppi_cmd/sessionB.cmd -v
WARNING:log_parser:Requested scan of J0154+1833 for 1440 sec at 1410 MHz [line=213] was not executed.
WARNING:log_parser:Requested scan of J0154+1833 for 1440 sec at 1410 MHz [line=213]: parfile "/home/gpu/tzpar/0154+1853.par" does not match source "J0154+1833"
WARNING:log_parser:Requested scan of J0154+1833 for 1440 sec at 430 MHz [line=221]: parfile "/home/gpu/tzpar/0154+1853.par" does not match source "J0154+1833"
Request PSR J1640+2224 for 1290s at 1410MHz at linenumber    12 
Request PSR J1640+2224 for 1290s at  430MHz at linenumber    24 
Request PSR J1630+3550 for 1290s at  430MHz at linenumber    33 
Request PSR J1630+3550 for 1290s at 1410MHz at linenumber    42 
Request PSR J1745+1017 for 1290s at 2030MHz at linenumber    51 
Request PSR J1745+1017 for 1290s at 1410MHz at linenumber    60 
Request PSR J1853+1303 for 1290s at 1410MHz at linenumber    69 
Request PSR J1853+1303 for 1290s at  430MHz at linenumber    78 
Request PSR B1855+09   for 1290s at  430MHz at linenumber    87 
Request PSR B1855+09   for 1290s at 1410MHz at linenumber    96 
Request PSR J1911+1347 for 1290s at 1410MHz at linenumber   105 
Request PSR J1911+1347 for 1290s at  430MHz at linenumber   114 
Request PSR J2017+0603 for 1440s at 2030MHz at linenumber   123 
Request PSR J2017+0603 for 1440s at 1410MHz at linenumber   132 
Request PSR J2043+1711 for 1440s at 1410MHz at linenumber   141 
Request PSR J2043+1711 for 1440s at  430MHz at linenumber   150 
Request PSR J2234+0944 for 1440s at 2030MHz at linenumber   159 
Request PSR J2234+0944 for 1440s at 1410MHz at linenumber   168 
Request PSR J2317+1439 for 1440s at 1410MHz at linenumber   177 
Request PSR J2317+1439 for 1440s at  430MHz at linenumber   186 
Request PSR J0023+0923 for 1440s at  430MHz at linenumber   195 
Request PSR J0023+0923 for 1440s at 1410MHz at linenumber   204 
Request PSR J0154+1833 for 1440s at 1410MHz at linenumber   213 *
Request PSR J0154+1833 for 1440s at  430MHz at linenumber   221 *
```

Makes sure all of the sessions will be executed, and that the `.par` files match the pulsars.  Those that don't pass are flagged in the output.

Output can be directed to a file.

## CIMA Logs
```
parse_cimalog -h
usage: parse_cimalog [-h] [--file FILE [FILE ...]] [--directory DIRECTORY]
                     [--programs PROGRAMS [PROGRAMS ...]] [--days DAYS]
                     [--tolerance TOLERANCE] [--email EMAIL] [--out OUT]
                     [--verbose]

Parse an Arecibo CIMA log file

optional arguments:
  -h, --help            show this help message and exit
  --file FILE [FILE ...], -f FILE [FILE ...]
                        Name(s) of CIMA log file(s) (default: None)
  --directory DIRECTORY, -d DIRECTORY
                        Directory to search for log files (default: ./)
  --programs PROGRAMS [PROGRAMS ...], -p PROGRAMS [PROGRAMS ...]
                        Observing programs to look for (default: ['p2945',
                        'p2780'])
  --days DAYS, -t DAYS  Days in the past to look for log files (<=0: find all)
                        (default: 1)
  --tolerance TOLERANCE
                        Tolerance for printing out exposure difference marks
                        (default: 100)
  --out OUT, -o OUT     Output destination (default: stdout)
  --verbose, -v         Increase verbosity (default: 0)
```

```
parse_cimalog -f examples/logs/p2780.cimalog_20200214 -v
INFO:log_parser:Looking at examples/logs/p2780.cimalog_20200214 ...
INFO:log_parser:CIMA session for p2780 with operator Daniel Padilla started at 2020-02-14 07:23:28
INFO:log_parser:Starting to track PSR J1741+1351 at 2020-02-14 07:26:01
INFO:log_parser:Ending tracking of J1741+1351 at 2020-02-14 07:28:19 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 07:28:40 line = 656
INFO:log_parser:Ending pulsar observation at 2020-02-14 07:53:03 line = 903
INFO:log_parser:Starting to track PSR J1741+1351 at 2020-02-14 07:54:13
INFO:log_parser:Ending tracking of J1741+1351 at 2020-02-14 07:54:21 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 07:54:32 line = 1315
INFO:log_parser:Ending pulsar observation at 2020-02-14 08:18:49 line = 1564
INFO:log_parser:Starting to track PSR J1803+1358 at 2020-02-14 08:19:01
INFO:log_parser:Ending tracking of J1803+1358 at 2020-02-14 08:20:40 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 08:20:47 line = 1909
INFO:log_parser:Ending pulsar observation at 2020-02-14 08:45:05 line = 2156
INFO:log_parser:Starting to track PSR J1803+1358 at 2020-02-14 08:46:01
INFO:log_parser:Ending tracking of J1803+1358 at 2020-02-14 08:46:09 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 08:46:26 line = 2595
INFO:log_parser:Ending pulsar observation at 2020-02-14 09:10:47 line = 2842
INFO:log_parser:Starting to track PSR J1923+2515 at 2020-02-14 09:10:58
INFO:log_parser:Ending tracking of J1923+2515 at 2020-02-14 09:17:43 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 09:18:00 line = 3215
INFO:log_parser:Ending pulsar observation at 2020-02-14 09:41:50 line = 3462
INFO:log_parser:Starting to track PSR J1923+2515 at 2020-02-14 09:42:53
INFO:log_parser:Ending tracking of J1923+2515 at 2020-02-14 09:43:01 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 09:43:12 line = 3874
INFO:log_parser:Ending pulsar observation at 2020-02-14 10:06:59 line = 4123
INFO:log_parser:Starting to track PSR B1937+21 at 2020-02-14 10:07:10
INFO:log_parser:Ending tracking of B1937+21 at 2020-02-14 10:09:06 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 10:09:13 line = 4468
INFO:log_parser:Ending pulsar observation at 2020-02-14 10:28:09 line = 4715
INFO:log_parser:Starting to track PSR J1946+3417 at 2020-02-14 10:28:20
INFO:log_parser:Ending tracking of J1946+3417 at 2020-02-14 10:33:35 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 10:33:46 line = 5060
INFO:log_parser:Ending pulsar observation at 2020-02-14 11:20:13 line = 5309
INFO:log_parser:Starting to track PSR B1953+29 at 2020-02-14 11:20:24
INFO:log_parser:Ending tracking of B1953+29 at 2020-02-14 11:22:36 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 11:22:46 line = 5654
INFO:log_parser:Ending pulsar observation at 2020-02-14 11:46:33 line = 5903
INFO:log_parser:Starting to track PSR B1953+29 at 2020-02-14 11:47:31
INFO:log_parser:Ending tracking of B1953+29 at 2020-02-14 11:47:39 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 11:47:59 line = 6342
WARNING:log_parser:Aborting current scan on target PSR B1953+29 at 2020-02-14 12:07:30 at line 6641 (started at 2020-02-14 11:47:31; tracking duration 1199s)
INFO:log_parser:Ending pulsar observation at 2020-02-14 12:07:38 line = 6675
INFO:log_parser:Starting to track PSR J2022+2534 at 2020-02-14 12:08:45
INFO:log_parser:Ending tracking of J2022+2534 at 2020-02-14 12:10:47 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 12:10:59 line = 7109
WARNING:log_parser:Aborting current scan on target PSR J2022+2534 at 2020-02-14 12:33:37 at line 7376 (started at 2020-02-14 12:08:45; tracking duration 1492s)
INFO:log_parser:Ending pulsar observation at 2020-02-14 12:33:46 line = 7408
INFO:log_parser:Starting to track PSR J2214+3000 at 2020-02-14 12:34:03
INFO:log_parser:Ending tracking of J2214+3000 at 2020-02-14 12:38:00 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 12:38:10 line = 7770
INFO:log_parser:Ending pulsar observation at 2020-02-14 13:29:37 line = 8019
INFO:log_parser:Starting to track PSR J2229+2643 at 2020-02-14 13:29:48
INFO:log_parser:Ending tracking of J2229+2643 at 2020-02-14 13:31:39 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 13:31:46 line = 8364
INFO:log_parser:Ending pulsar observation at 2020-02-14 13:58:02 line = 8611
INFO:log_parser:Starting to track PSR J2229+2643 at 2020-02-14 13:59:03
INFO:log_parser:Ending tracking of J2229+2643 at 2020-02-14 13:59:10 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 13:59:30 line = 9051
INFO:log_parser:Ending pulsar observation at 2020-02-14 14:25:52 line = 9298
INFO:log_parser:Starting to track PSR J2322+2057 at 2020-02-14 14:26:03
INFO:log_parser:Ending tracking of J2322+2057 at 2020-02-14 14:31:11 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 14:31:32 line = 9673
INFO:log_parser:Ending pulsar observation at 2020-02-14 14:57:55 line = 9920
INFO:log_parser:Starting to track PSR J2322+2057 at 2020-02-14 14:58:58
INFO:log_parser:Ending tracking of J2322+2057 at 2020-02-14 14:59:06 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 14:59:14 line = 10332
INFO:log_parser:Ending pulsar observation at 2020-02-14 15:25:31 line = 10579
INFO:log_parser:Starting to track PSR J0030+0451 at 2020-02-14 15:25:42
INFO:log_parser:Ending tracking of J0030+0451 at 2020-02-14 15:29:42 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 15:29:51 line = 10928
INFO:log_parser:Ending pulsar observation at 2020-02-14 15:56:07 line = 11175
INFO:log_parser:Starting to track PSR J0030+0451 at 2020-02-14 15:57:07
INFO:log_parser:Ending tracking of J0030+0451 at 2020-02-14 15:57:14 with status OK
INFO:log_parser:Starting pulsar observation (std) at 2020-02-14 15:57:32 line = 11615
INFO:log_parser:Ending pulsar observation at 2020-02-14 16:24:03 line = 11931
### Report for: examples/logs/p2780.cimalog_20200214
### NANOGrav p2780 observation (9.0h elapsed; 8.1h observing; 18 scans)
### 2020-02-14 07:23:28 - 2020-02-14 16:24:17
 312.0 sec --> Execute PSR J1741+1351 (std) for 1463s at  430MHz at linenumber   656 (1320.0 sec requested) +
  89.0 sec --> Execute PSR J1741+1351 (std) for 1457s at 1410MHz at linenumber  1315 (1320.0 sec requested) +
 118.0 sec --> Execute PSR J1803+1358 (std) for 1458s at 1410MHz at linenumber  1909 (1320.0 sec requested) +
  81.0 sec --> Execute PSR J1803+1358 (std) for 1461s at  430MHz at linenumber  2595 (1320.0 sec requested) +
 433.0 sec --> Execute PSR J1923+2515 (std) for 1430s at  430MHz at linenumber  3215 (1290.0 sec requested) +
  82.0 sec --> Execute PSR J1923+2515 (std) for 1427s at 1410MHz at linenumber  3874 (1290.0 sec requested) +
 134.0 sec --> Execute PSR B1937+21   (std) for 1136s at 1410MHz at linenumber  4468 (1000.0 sec requested) +
 337.0 sec --> Execute PSR J1946+3417 (std) for 2787s at 1410MHz at linenumber  5060 (2650.0 sec requested) +
 153.0 sec --> Execute PSR B1953+29   (std) for 1427s at 1410MHz at linenumber  5654 (1290.0 sec requested) +
  86.0 sec --> Execute PSR B1953+29   (std) for 1179s at  430MHz at linenumber  6342 (1290.0 sec requested) -
 201.0 sec --> Execute PSR J2022+2534 (std) for 1367s at 1410MHz at linenumber  7109 (2650.0 sec requested) ------------
 264.0 sec --> Execute PSR J2214+3000 (std) for 3087s at 1410MHz at linenumber  7770 (2950.0 sec requested) +
 129.0 sec --> Execute PSR J2229+2643 (std) for 1576s at 1410MHz at linenumber  8364 (1440.0 sec requested) +
  88.0 sec --> Execute PSR J2229+2643 (std) for 1582s at  430MHz at linenumber  9051 (1440.0 sec requested) +
 340.0 sec --> Execute PSR J2322+2057 (std) for 1583s at  430MHz at linenumber  9673 (1440.0 sec requested) +
  79.0 sec --> Execute PSR J2322+2057 (std) for 1577s at 1410MHz at linenumber 10332 (1440.0 sec requested) +
 260.0 sec --> Execute PSR J0030+0451 (std) for 1576s at 1410MHz at linenumber 10928 (1440.0 sec requested) +
  85.0 sec --> Execute PSR J0030+0451 (std) for 1591s at  430MHz at linenumber 11615 (1440.0 sec requested) +
```

Options:
* Can specify files directly, or by looking back `--days` in a directory
* Will only look for logs of the specified programs
* Can write to a file instead of `stdout`

# LogParse 

Methods to parse Arecibo PUPPI command files and CIMA logs.

## Command files:
```python
import log_parser
c=log_parser.Command_Parser('sessionB.cmd')
print(c)
PUPPI commands from sessionC_No-S.cmd, using catalog nanograv.cat, total time to execute: 28330s
Observe PSR J1741+1351 for 1320s at 430MHz
Observe PSR J1741+1351 for 1320s at 1410MHz
Observe PSR J1803+1358 for 1320s at 1410MHz
Observe PSR J1803+1358 for 1320s at 430MHz
Observe PSR J1923+2515 for 1290s at 430MHz
Observe PSR J1923+2515 for 1290s at 1410MHz
Observe PSR B1937+21 for 1000s at 1410MHz
Observe PSR J1946+3417 for 2650s at 1410MHz
Observe PSR B1953+29 for 1290s at 1410MHz
Observe PSR B1953+29 for 1290s at 430MHz
Observe PSR J2022+2534 for 2650s at 1410MHz
Observe PSR J2214+3000 for 2950s at 1410MHz
Observe PSR J2229+2643 for 1440s at 1410MHz
Observe PSR J2229+2643 for 1440s at 430MHz
Observe PSR J2322+2057 for 1440s at 430MHz
Observe PSR J2322+2057 for 1440s at 1410MHz
Observe PSR J0030+0451 for 1440s at 1410MHz
Observe PSR J0030+0451 for 1440s at 430MHz
```

## CIMA Logs
```python
import log_parser
c=Log_Parser('p2780.cimalog_20200214')
### NANOGrav p2780 observation (9.0h elapsed; 8.1h observing; 18 scans)
### 2020-Feb-14T07:23:28 - 2020-Feb-14T16:23:54
   312 sec --> Execute PSR J1741+1351 for 1463s at 430MHz at linenumber 202-212 (1320 sec requested)
    89 sec --> Execute PSR J1741+1351 for 1457s at 1410MHz at linenumber 905-913 (1320 sec requested)
   118 sec --> Execute PSR J1803+1358 for 1458s at 1410MHz at linenumber 1566-1574 (1320 sec requested)
    81 sec --> Execute PSR J1803+1358 for 1461s at 430MHz at linenumber 2158-2166 (1320 sec requested)
   432 sec --> Execute PSR J1923+2515 for 1431s at 430MHz at linenumber 2844-2852 (1290 sec requested)
    82 sec --> Execute PSR J1923+2515 for 1427s at 1410MHz at linenumber 3464-3472 (1290 sec requested)
   134 sec --> Execute PSR B1937+21 for 1136s at 1410MHz at linenumber 4125-4133 (1000 sec requested)
   337 sec --> Execute PSR J1946+3417 for 2787s at 1410MHz at linenumber 4717-4725 (2650 sec requested)
   153 sec --> Execute PSR B1953+29 for 1427s at 1410MHz at linenumber 5311-5319 (1290 sec requested)
    86 sec --> Execute PSR B1953+29 for 1171s at 430MHz at linenumber 5905-5913 (1290 sec requested)
   209 sec --> Execute PSR J2022+2534 for 1358s at 1410MHz at linenumber 6692-6700 (2650 sec requested)
   273 sec --> Execute PSR J2214+3000 for 3087s at 1410MHz at linenumber 7425-7433 (2950 sec requested)
   129 sec --> Execute PSR J2229+2643 for 1576s at 1410MHz at linenumber 8021-8029 (1440 sec requested)
    88 sec --> Execute PSR J2229+2643 for 1582s at 430MHz at linenumber 8613-8621 (1440 sec requested)
   339 sec --> Execute PSR J2322+2057 for 1584s at 430MHz at linenumber 9300-9308 (1440 sec requested)
    79 sec --> Execute PSR J2322+2057 for 1577s at 1410MHz at linenumber 9922-9930 (1440 sec requested)
   259 sec --> Execute PSR J0030+0451 for 1577s at 1410MHz at linenumber 10581-10589 (1440 sec requested)
    85 sec --> Execute PSR J0030+0451 for 1582s at 430MHz at linenumber 11177-11185 (1440 sec requested)
```
## Dependencies:
All standard python, 2 (>=2.7) or 3: re, logging, datetime, sys, json, collections, os

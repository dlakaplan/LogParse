# LogParse 

Methods to parse Arecibo PUPPI command files and CIMA logs.

## Command files:
```python
import log_parser
c=log_parser.CIMA_Command_Parser('sessionB.cmd')
print(c)
```
~~~
CIMA commands from sessionB.cmd, using catalog nanograv.cat, total time to execute: 31320s
Request PSR J1640+2224 for 1290s at 1410MHz at linenumber    12 -    23
Request PSR J1640+2224 for 1290s at  430MHz at linenumber    24 -    32
Request PSR J1630+3550 for 1290s at  430MHz at linenumber    33 -    41
Request PSR J1630+3550 for 1290s at 1410MHz at linenumber    42 -    50
Request PSR J1745+1017 for 1290s at 2030MHz at linenumber    51 -    59
Request PSR J1745+1017 for 1290s at 1410MHz at linenumber    60 -    68
Request PSR J1853+1303 for 1290s at 1410MHz at linenumber    69 -    77
Request PSR J1853+1303 for 1290s at  430MHz at linenumber    78 -    86
Request PSR B1855+09   for 1290s at  430MHz at linenumber    87 -    95
Request PSR B1855+09   for 1290s at 1410MHz at linenumber    96 -   104
Request PSR J1911+1347 for 1290s at 1410MHz at linenumber   105 -   113
Request PSR J1911+1347 for 1290s at  430MHz at linenumber   114 -   122
Request PSR J2017+0603 for 1440s at 2030MHz at linenumber   123 -   131
Request PSR J2017+0603 for 1440s at 1410MHz at linenumber   132 -   140
Request PSR J2043+1711 for 1440s at 1410MHz at linenumber   141 -   149
Request PSR J2043+1711 for 1440s at  430MHz at linenumber   150 -   158
Request PSR J2234+0944 for 1440s at 2030MHz at linenumber   159 -   167
Request PSR J2234+0944 for 1440s at 1410MHz at linenumber   168 -   176
Request PSR J2317+1439 for 1440s at 1410MHz at linenumber   177 -   185
Request PSR J2317+1439 for 1440s at  430MHz at linenumber   186 -   194
Request PSR J0023+0923 for 1440s at  430MHz at linenumber   195 -   203
Request PSR J0023+0923 for 1440s at 1410MHz at linenumber   204 -   212
Request PSR J0154+1833 for 1440s at 1410MHz at linenumber   213 -   220
Request PSR J0154+1833 for 1440s at  430MHz at linenumber   221 -   229
~~~

## CIMA Logs
```python
import log_parser
c=log_parser.CIMA_Log_Parser('p2780.cimalog_20200214')
```
~~~
### NANOGrav p2780 observation (11.4h elapsed; 7.3h observing; 20 scans)
### 2020-Feb-22T04:31:37 - 2020-Feb-22T15:55:47
..5977 sec --> Execute PSR J1640+2224 for    1s at 1410MHz at linenumber  1236 -  1243 (1290 sec requested) ---
...490 sec --> Execute PSR J1640+2224 for 1427s at 1410MHz at linenumber  3376 -  3386 (1290 sec requested) 
....86 sec --> Execute PSR J1640+2224 for 1428s at  430MHz at linenumber  4049 -  4057 (1290 sec requested) 
...369 sec --> Execute PSR J1630+3550 for 1428s at  430MHz at linenumber  4736 -  4744 (1290 sec requested) 
..1672 sec --> Execute PSR J1745+1017 for 1427s at 2030MHz at linenumber  5829 -  5837 (1290 sec requested) 
...150 sec --> Execute PSR J1745+1017 for 1426s at 1410MHz at linenumber  6493 -  6501 (1290 sec requested) 
...257 sec --> Execute PSR J1853+1303 for 1427s at 1410MHz at linenumber  7214 -  7222 (1290 sec requested) 
....87 sec --> Execute PSR J1853+1303 for 1433s at  430MHz at linenumber  7808 -  7816 (1290 sec requested) 
....83 sec --> Execute PSR B1855+09   for 1431s at  430MHz at linenumber  8495 -  8503 (1290 sec requested) 
....79 sec --> Execute PSR B1855+09   for 1077s at 1410MHz at linenumber  9116 -  9124 (1290 sec requested) ---
...134 sec --> Execute PSR J1911+1347 for 1216s at 1410MHz at linenumber  9852 -  9860 (1290 sec requested) 
..1251 sec --> Execute PSR J2017+0603 for 1577s at 2030MHz at linenumber 10936 - 10944 (1440 sec requested) 
..1490 sec --> Execute PSR J2043+1711 for 1576s at 1410MHz at linenumber 12072 - 12080 (1440 sec requested) 
..1230 sec --> Execute PSR J2234+0944 for 1577s at 2030MHz at linenumber 13748 - 13756 (1440 sec requested) 
...130 sec --> Execute PSR J2234+0944 for 1576s at 1410MHz at linenumber 14370 - 14378 (1440 sec requested) 
...287 sec --> Execute PSR J2317+1439 for 1576s at 1410MHz at linenumber 15029 - 15037 (1440 sec requested) 
....94 sec --> Execute PSR J2317+1439 for 1583s at  430MHz at linenumber 15623 - 15631 (1440 sec requested) 
...242 sec --> Execute PSR J0023+0923 for 1582s at  430MHz at linenumber 16316 - 16324 (1440 sec requested) 
....79 sec --> Execute PSR J0023+0923 for 1577s at 1410MHz at linenumber 16907 - 16915 (1440 sec requested) 
...508 sec --> Execute PSR J0154+1833 for   10s at  430MHz at linenumber 17911 - 17919 (1440 sec requested) ---
~~~

## Dependencies:
All standard python, 2 (>=2.7) or 3: re, logging, datetime, sys, json, collections, os

# P2780 "B" session schedule
# ZA 1 January 2016, based on DJN's email of 12/28/15 describing the
# latest P2780 proposal session definitions
#
# File commands include some redundant SETUP, SEEK, and LOAD commands
# This will add a small amount to the observing time (primarily the
#    redundant LOAD commands).  However, it will greatly simplify any
#    emergency cut-and-paste rewriting of this script during an
#    observing session.

catalog nanograv.cat

LOAD cima_control_puppi_430.conf
SEEK J1640+2224
EXEC change_puppi_parfile "/home/gpu/tzpar/1640+2224.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1290 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

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

LOAD cima_control_puppi_1410.conf
SEEK J1630+3550
EXEC change_puppi_parfile "/home/gpu/tzpar/1630+3550.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1630+3550
EXEC change_puppi_parfile "/home/gpu/tzpar/1630+3550.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1745+1017
EXEC change_puppi_parfile "/home/gpu/tzpar/1745+1017.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1745+1017
EXEC change_puppi_parfile "/home/gpu/tzpar/1745+1017.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1853+1303
EXEC change_puppi_parfile "/home/gpu/tzpar/1853+1303.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1853+1303
EXEC change_puppi_parfile "/home/gpu/tzpar/1853+1303.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK B1855+09
EXEC change_puppi_parfile "/home/gpu/tzpar/1855+09.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK B1855+09
EXEC change_puppi_parfile "/home/gpu/tzpar/1855+09.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1911+1347
EXEC change_puppi_parfile "/home/gpu/tzpar/1911+1347.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1911+1347
EXEC change_puppi_parfile "/home/gpu/tzpar/1911+1347.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J2017+0603
EXEC change_puppi_parfile "/home/gpu/tzpar/2017+0603.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2017+0603
EXEC change_puppi_parfile "/home/gpu/tzpar/2017+0603.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2043+1711
EXEC change_puppi_parfile "/home/gpu/tzpar/2043+1711.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J2043+1711
EXEC change_puppi_parfile "/home/gpu/tzpar/2043+1711.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J2234+0944
EXEC change_puppi_parfile "/home/gpu/tzpar/2234+0944.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2234+0944
EXEC change_puppi_parfile "/home/gpu/tzpar/2234+0944.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2317+1439
EXEC change_puppi_parfile "/home/gpu/tzpar/2317+1439.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J2317+1439
EXEC change_puppi_parfile "/home/gpu/tzpar/2317+1439.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J0023+0923
EXEC change_puppi_parfile "/home/gpu/tzpar/0023+0923.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0023+0923
EXEC change_puppi_parfile "/home/gpu/tzpar/0023+0923.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0154+1833
EXEC change_puppi_parfile "/home/gpu/tzpar/0154+1833.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J0154+1833
EXEC change_puppi_parfile "/home/gpu/tzpar/0154+1833.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

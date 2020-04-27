# P2780 "C" session schedule
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
EXEC vw_send "pnt wrap -1"
SEEK J1741+1351
EXEC vw_send "pnt wrap 0"
EXEC change_puppi_parfile "/home/gpu/tzpar/1741+1351.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1320 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1741+1351
EXEC change_puppi_parfile "/home/gpu/tzpar/1741+1351.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
#EXEC wait_puppi_temporary "180" "Check PUPPI power with guppi_adc_hist"
SETUP pulsaron secs=1320 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1803+1358
EXEC change_puppi_parfile "/home/gpu/tzpar/1803+1358.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1320 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1803+1358
EXEC change_puppi_parfile "/home/gpu/tzpar/1803+1358.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1320 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1923+2515
EXEC change_puppi_parfile "/home/gpu/tzpar/1923+2515.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1923+2515
EXEC change_puppi_parfile "/home/gpu/tzpar/1923+2515.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK B1937+21
EXEC change_puppi_parfile "/home/gpu/tzpar/1937+21.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=500 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK B1937+21
EXEC change_puppi_parfile "/home/gpu/tzpar/1937+21.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=500 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1946+3417
EXEC change_puppi_parfile "/home/gpu/tzpar/1946+3417.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1946+3417
EXEC change_puppi_parfile "/home/gpu/tzpar/1946+3417.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK B1953+29
EXEC change_puppi_parfile "/home/gpu/tzpar/1953+29.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK B1953+29
EXEC change_puppi_parfile "/home/gpu/tzpar/1953+29.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2022+2534
EXEC change_puppi_parfile "/home/gpu/tzpar/2022+2534.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J2022+2534
EXEC change_puppi_parfile "/home/gpu/tzpar/2022+2534.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1290 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J2214+3000
EXEC change_puppi_parfile "/home/gpu/tzpar/2214+3000.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
ADJUSTPOWER
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2214+3000
EXEC change_puppi_parfile "/home/gpu/tzpar/2214+3000.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
ADJUSTPOWER
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2229+2643
EXEC change_puppi_parfile "/home/gpu/tzpar/2229+2643.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
ADJUSTPOWER
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J2229+2643
EXEC change_puppi_parfile "/home/gpu/tzpar/2229+2643.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
ADJUSTPOWER
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J2322+2057
EXEC change_puppi_parfile "/home/gpu/tzpar/2322+2057.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
ADJUSTPOWER
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2322+2057
EXEC change_puppi_parfile "/home/gpu/tzpar/2322+2057.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
ADJUSTPOWER
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0030+0451
EXEC change_puppi_parfile "/home/gpu/tzpar/0030+0451.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J0030+0451
EXEC change_puppi_parfile "/home/gpu/tzpar/0030+0451.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1440 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

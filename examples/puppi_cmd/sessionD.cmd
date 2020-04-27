# P2780 "D" session schedule
# For use by Arecibo operator; interactive ADC hist check has been removed.
# Incoming data can be viewed at http://www.naic.edu/~puppi/puppi.shtml
#
# ZA 1 January 2016, based on DJN's email of 12/28/15 describing the
# latest P2780 proposal session definitions, and on ECF's command file 
# P2989_session_Hour5.cmd but with the first two sources swapped to 
# minimize slew time and avoid a potential wrap issue.
# 
# File commands include some redundant SETUP, SEEK, and LOAD commands
# This will add a small amount to the observing time (primarily the
#    redundant LOAD commands).  However, it will greatly simplify any
#    emergency cut-and-paste rewriting of this script during an
#    observing session.

catalog nanograv.cat

LOAD cima_control_puppi_1410.conf
SEEK J0406+3039
EXEC change_puppi_parfile "/home/gpu/tzpar/0406+3039.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
#EXEC wait_puppi_temporary "180" "Check PUPPI power levels"
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J0406+3039
EXEC change_puppi_parfile "/home/gpu/tzpar/0406+3039.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J0509+0856
EXEC change_puppi_parfile "/home/gpu/tzpar/0509+0856.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0509+0856
EXEC change_puppi_parfile "/home/gpu/tzpar/0509+0856.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
EXEC vw_send "pnt wrap -1"
SEEK J0557+1551
EXEC vw_send "pnt wrap 0"
EXEC change_puppi_parfile "/home/gpu/tzpar/0557+1551.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J0557+1551
EXEC change_puppi_parfile "/home/gpu/tzpar/0557+1551.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J0709+0458
EXEC change_puppi_parfile "/home/gpu/tzpar/0709+0458.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0709+0458
EXEC change_puppi_parfile "/home/gpu/tzpar/0709+0458.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0732+2314
EXEC change_puppi_parfile "/home/gpu/tzpar/0732+2314.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J0732+2314
EXEC change_puppi_parfile "/home/gpu/tzpar/0732+2314.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J0751+1807
EXEC change_puppi_parfile "/home/gpu/tzpar/0751+1807.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J0751+1807
EXEC change_puppi_parfile "/home/gpu/tzpar/0751+1807.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1022+1001
EXEC change_puppi_parfile "/home/gpu/tzpar/1022+1001.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1022+1001
EXEC change_puppi_parfile "/home/gpu/tzpar/1022+1001.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

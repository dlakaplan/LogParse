# P2780 "A" session schedule
# ZA 1 January 2016, based on DJN's email of 12/28/15 describing the
# latest P2780 proposal session definitions
#
# MD added J1327+3423 on Aug 4, 2018. Previous .cmd file (2018 Feb - 2018 Jul) is in other_cmd_files.
#
# **NOTE** Flux cal scans are now embedded in this session after the first 
# few pulsar scans. They require CONFIRMING PUPPI LEVELS for EACH frequency!
# 
# File commands include some redundant SETUP, SEEK, and LOAD commands
# This will add a small amount to the observing time (primarily the
#    redundant LOAD commands).  However, it will greatly simplify any
#    emergency cut-and-paste rewriting of this script during an
#    observing session.

catalog nanograv.cat

LOAD cima_control_puppi_1410.conf
EXEC vw_send "pnt wrap -1"
SEEK B1257+12
EXEC vw_send "pnt wrap 0"
EXEC change_puppi_parfile "/home/gpu/tzpar/B1257+12.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
#EXEC wait_puppi_temporary "180" "Check PUPPI power levels"
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK B1257+12
EXEC change_puppi_parfile "/home/gpu/tzpar/B1257+12.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1312+0051
EXEC change_puppi_parfile "/home/gpu/tzpar/1312+0051.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1110 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1312+0051
EXEC change_puppi_parfile "/home/gpu/tzpar/1312+0051.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1110 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1327+3423
EXEC change_puppi_parfile "/home/gpu/tzpar/J1327+3423.par"
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1110 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1327+3423
EXEC change_puppi_parfile "/home/gpu/tzpar/J1327+3423.par"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
ADJUSTPOWER
SETUP pulsaron secs=1110 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1445+099
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
EXEC ponoffcal "300" "lcorcal" "5" "azza" 

LOAD cima_control_puppi_2030.conf
SEEK J1445+099
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
EXEC ponoffcal "300" "lcorcal" "5" "azza" 

LOAD cima_control_puppi_1410.conf
SEEK J1445+099
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
EXEC ponoffcal "300" "lcorcal" "5" "azza" 

LOAD cima_control_puppi_1410.conf
SEEK J1453+1902
EXEC change_puppi_parfile "/home/gpu/tzpar/1453+1902.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1453+1902
EXEC change_puppi_parfile "/home/gpu/tzpar/1453+1902.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
EXEC vw_send "pnt wrap -1"
SEEK J1713+0747
EXEC vw_send "pnt wrap 0"
EXEC change_puppi_parfile "/home/gpu/tzpar/1713+0747.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1713+0747
EXEC change_puppi_parfile "/home/gpu/tzpar/1713+0747.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1738+0333
EXEC change_puppi_parfile "/home/gpu/tzpar/1738+0333.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1738+0333
EXEC change_puppi_parfile "/home/gpu/tzpar/1738+0333.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1910+1256
EXEC change_puppi_parfile "/home/gpu/tzpar/1910+1256.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1910+1256
EXEC change_puppi_parfile "/home/gpu/tzpar/1910+1256.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1903+0327
EXEC change_puppi_parfile "/home/gpu/tzpar/1903+0327.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
SEEK J1903+0327
EXEC change_puppi_parfile "/home/gpu/tzpar/1903+0327.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J1944+0907
EXEC change_puppi_parfile "/home/gpu/tzpar/1944+0907.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J1944+0907
EXEC change_puppi_parfile "/home/gpu/tzpar/1944+0907.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J2033+1734
EXEC change_puppi_parfile "/home/gpu/tzpar/2033+1734.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2033+1734
EXEC change_puppi_parfile "/home/gpu/tzpar/2033+1734.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2234+0611
EXEC change_puppi_parfile "/home/gpu/tzpar/2234+0611.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_430.conf
SEEK J2234+0611
EXEC change_puppi_parfile "/home/gpu/tzpar/2234+0611.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048"
SETUP pulsaron secs=1140 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

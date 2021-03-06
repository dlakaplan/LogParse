# P2945 CIMA command file for J1713+0747
# Written by E. Fonseca on 30 December 2014
# Edits:
#   - ...

catalog nanograv2.cat

LOAD cima_control_puppi_1410.conf
#EXEC vw_send "pnt wrap -1"
SEEK J1713+0747
EXEC vw_send "pnt wrap 0"
EXEC change_puppi_parfile "/home/gpu/tzpar/1713+0747.par"
ADJUSTPOWER
#EXEC wait_puppi_temporary "180" "Check PUPPI power with guppi_adc_hist."
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_2030.conf
#EXEC vw_send "pnt wrap 0"
SEEK J1713+0747
EXEC change_puppi_parfile "/home/gpu/tzpar/1713+0747.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=1260 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

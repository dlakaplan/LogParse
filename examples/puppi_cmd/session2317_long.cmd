# P2945 CIMA command file for J2317+1439
# Written by E. Fonseca on 30 December 2014.
# Edits:
#   - ...

catalog nanograv2.cat

LOAD cima_control_puppi_430.conf
# EXEC vw_send "pnt wrap 1"
SEEK J2317+1439
EXEC change_puppi_parfile "/home/gpu/tzpar/2317+1439.par"
ADJUSTPOWER
EXEC wait_puppi_temporary "180" "Check PUPPI power with guppi_adc_hist"
EXEC change_puppi_dumptime "FOLD" "1" "2048"
EXEC change_puppi_dumptime "CAL" "1" "2048" 
SETUP pulsaron secs=1680 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

LOAD cima_control_puppi_1410.conf
SEEK J2317+1439
EXEC change_puppi_parfile "/home/gpu/tzpar/2317+1439.par"
ADJUSTPOWER
EXEC change_puppi_dumptime "FOLD" "10" "2048"
EXEC change_puppi_dumptime "CAL" "10" "2048" 
SETUP pulsaron secs=2000 loops=1 caltype=winkcal calsecs=90 calmode=on winkcal=off winkcaltype=lcorcal adjpwr=never newfile=one
PULSARON

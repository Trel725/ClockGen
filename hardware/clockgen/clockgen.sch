EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L 2021-08-26_08-32-07:74ALVC164245DLG4 U?
U 1 1 61275A01
P 4000 2750
F 0 "U?" H 5200 3137 60  0000 C CNN
F 1 "74ALVC164245DLG4" H 5200 3031 60  0000 C CNN
F 2 "DL48" H 5200 2990 60  0001 C CNN
F 3 "" H 4000 2750 60  0000 C CNN
	1    4000 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7450 3500 7400 3500
Wire Wire Line
	6400 3500 6400 3550
Wire Wire Line
	7450 3600 7400 3600
Wire Wire Line
	6400 3600 6400 3650
Wire Wire Line
	7450 3700 7400 3700
Wire Wire Line
	6400 3700 6400 3750
Wire Wire Line
	7400 4750 7400 4700
$Comp
L arduino:Arduino_Uno_Shield XA?
U 1 1 61277613
P 8700 3850
F 0 "XA?" H 8700 5237 60  0000 C CNN
F 1 "Arduino_Uno_Shield" H 8700 5131 60  0000 C CNN
F 2 "" H 10500 7600 60  0001 C CNN
F 3 "https://store.arduino.cc/arduino-uno-rev3" H 10500 7600 60  0001 C CNN
	1    8700 3850
	1    0    0    -1  
$EndComp
Connection ~ 7400 3500
Wire Wire Line
	7400 3500 6400 3500
Connection ~ 7400 3600
Wire Wire Line
	7400 3600 6400 3600
Connection ~ 7400 3700
Wire Wire Line
	7400 3700 6400 3700
$EndSCHEMATC

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
L 2021-08-26_08-32-07:74ALVC164245DLG4 U1
U 1 1 61275A01
P 3000 3100
F 0 "U1" H 4200 3487 60  0000 C CNN
F 1 "74ALVC164245DLG4" H 4200 3381 60  0000 C CNN
F 2 "footprints:74ALVC164245DLG4" H 4200 3340 60  0001 C CNN
F 3 "" H 3000 3100 60  0000 C CNN
	1    3000 3100
	1    0    0    -1  
$EndComp
Text Label 5400 3200 0    50   ~ 0
A1
Text Label 5400 3300 0    50   ~ 0
A2
Text Label 7250 3400 0    50   ~ 0
A5
Text Label 7250 3500 0    50   ~ 0
A4
Text Label 5400 3500 0    50   ~ 0
A3
Text Label 5400 3600 0    50   ~ 0
A4
Text Label 5400 3800 0    50   ~ 0
A5
Text Label 5400 3900 0    50   ~ 0
A6
Text Label 7250 3600 0    50   ~ 0
A3
Text Label 7250 3700 0    50   ~ 0
A2
Text Label 7250 3800 0    50   ~ 0
A1
Text Label 7250 3900 0    50   ~ 0
A0
Text Label 5400 3400 0    50   ~ 0
GND
Text Label 5400 3700 0    50   ~ 0
GND
Text Label 5400 4000 0    50   ~ 0
GND
$Comp
L power:GND #PWR0101
U 1 1 612D9330
P 7000 4400
F 0 "#PWR0101" H 7000 4150 50  0001 C CNN
F 1 "GND" H 7005 4227 50  0000 C CNN
F 2 "" H 7000 4400 50  0001 C CNN
F 3 "" H 7000 4400 50  0001 C CNN
	1    7000 4400
	1    0    0    -1  
$EndComp
$Comp
L arduino:Arduino_Uno_Shield_no_ICSP XA1
U 1 1 61298011
P 8550 3750
F 0 "XA1" H 8550 5137 60  0000 C CNN
F 1 "Arduino_Uno_Shield_no_ICSP" H 8550 5031 60  0000 C CNN
F 2 "Arduino:Arduino_Uno_Connector" H 10350 7500 60  0001 C CNN
F 3 "https://store.arduino.cc/arduino-uno-rev3" H 10350 7500 60  0001 C CNN
	1    8550 3750
	1    0    0    -1  
$EndComp
Wire Wire Line
	7250 4300 7150 4300
Wire Wire Line
	7000 4300 7000 4400
Wire Wire Line
	7250 4400 7150 4400
Wire Wire Line
	7150 4400 7150 4300
Connection ~ 7150 4300
Wire Wire Line
	7150 4300 7000 4300
Wire Wire Line
	7250 4500 7150 4500
Wire Wire Line
	7150 4500 7150 4400
Connection ~ 7150 4400
Text Label 3000 4000 2    50   ~ 0
GND
Text Label 3000 4500 2    50   ~ 0
GND
Text Label 3000 5100 2    50   ~ 0
GND
Text Label 5400 4100 0    50   ~ 0
D2
Text Label 5400 4200 0    50   ~ 0
D3
Text Label 5400 4300 0    50   ~ 0
D4
Text Label 5400 4400 0    50   ~ 0
D5
Text Label 5400 4600 0    50   ~ 0
D6
Text Label 5400 4700 0    50   ~ 0
D7
Text Label 5400 4500 0    50   ~ 0
GND
Text Label 5400 4800 0    50   ~ 0
VCC_33
Text Label 5400 4900 0    50   ~ 0
D8
Text Label 5400 5000 0    50   ~ 0
D9
Text Label 5400 5200 0    50   ~ 0
D10
Text Label 5400 5300 0    50   ~ 0
D11
Text Label 5400 5400 0    50   ~ 0
D12
Text Label 5400 5100 0    50   ~ 0
GND
$EndSCHEMATC

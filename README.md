# ClockGen

## What's that?

ClockGen is a project, devoted to developing a device that allow simple synchronization of scientific equipment. When experiments require synchronization, one might select do it with Arduino or similar hardware (LabJack?) which would give millisecond accuracy, or go far beyond that to specialized timing equipment, able of generating nanosecond precise pulses and costing thousands of euro. The goal of that project is to provide "something in between", a device which can provide microsecond accuracy at reasonable price. The devise is based on STM32F446RET Nucleo development board (price below 20 euro).

## Features?

 - Generating square wave at frequencies from 610 Hz (for 16 bit timer) or 0.009 Hz (for 32 bit timer) up to ~ 10 MHz
 - Programming arbitrary sequences of start, stop or change frequency events at 1 us accuracy 
 - Support of up to 10 timer channels for generating square wave
 - Synchronization of the generated signals with nanosecond accuracy by hardware synchronization
 - Up to 22 digital outputs, programmable to generate arbitrary sequences of on/off events with 1 us accuracy and nanosecond synchronization 
 - Hardware extension for Nucleo development board, converting LVTTL signals from microcontroller (3.3V) to standard TTL (5V)
 - Add-on hardware extension, converting 5V TTL signals to high-voltage signals (7-18V).


## How to use it

```python
from clockgen import ProgramGen
from clockgen.interface import TIM, GPIO
from clockgen.utils import send_program, start_execution

#instantiate HW
tim2 = TIM("TIM2")
tim5 = TIM("TIM5")
gpa = GPIO("GPIOA")

# turn on both timers at time 100us from program start
# tim2 at 20 kHz
tim2.on_sync(20_000, 100)
# and tim5 at 10 kHz
tim5.on_sync(10_000, 100)
# start them synchnously
tim1.start_sync(100)

# set 4th and 6th pins in GPIOA to high level at 120 us
gpa.on([4, 6], 120)
# then pin 4 to low level at 150 us
gpa.off(4, 150)
# and pin 6 at 900 us
gpa.off(6, 900)

# finally turn off the timers at 1000 us
tim1.off_sync(1000)
tim2.off_sync(1000)

# instantiate program generator
pg = ProgramGen()
# and generate the program, providing it list of used HW
prog = pg.generate_program([gpa, tim2, tim5])
# open the serial connection
ser = serial.Serial("/dev/ttyACM0", baudrate=1000000, timeout=5)
# and send the program to microntroller
send_program(prog)
# and start its execution:
start_execution()
```


Also, see folder examples.

## How does it work?

1. User describes the desired sequence of operations, like start signal generation at PA0 at 300 us.
2. Host-side program keeps track of all register changes and thus translates high-level operations into low-level
register manipulation
3. Host compiles sequence of register manipilation actions into binary program for micontroller and sends the program.
4. Microcontroller stores the program in RAM and waits for the start_execution command. As soon as command is received, it starts execution and generates required sequence of signals.

## What do I need to start using the ClockGen
In the simpliest case - just STM32F446RET Nucleo development board. As soon as your equipment recognizes LVTTL (3.3V) logical levels, it should suffice. Still, majority of scientific equipment works with 5V TTL levels, and behaviour might be unpredictable if different logical levels is used, thus it is recommeded to get extension board, which converts the signals to 5V TTL. Moreover, it is capable to supply more current and electrically isolates microcontroller from high voltage spikes.
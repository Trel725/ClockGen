#list of available gpios
GPIO_LIST = ['GPIOA', 'GPIOB', "GPIOC", "GPIOD"]

# frequency of timers
TIM_FREQ = 80_000_000

# master timer, start of which causes start of all other timers
MASTER_TIMER = "TIM1"

# standard delay between timer start and its initialization
# e.g. if timer should start at t=10000, it will be initialized at
# 9990
TIM_INIT_DELAY = 10

# constants for program
# end of frame
EOF = 0xABBCCDDE
# end of programm
EOP = 0xFFFFFFFF

# constants for sending program
SERIAL_START = b'\x11'
SERIAL_END = b'\xa0'
SERIAL_EXECUTE = b'\xc6'
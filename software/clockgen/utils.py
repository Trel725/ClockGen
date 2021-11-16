import zlib
import warnings
from . import pin_mapping, hw_desc
from . import Timer
from .hw import GPIO
from .constants import (SERIAL_START, SERIAL_END, SERIAL_STOP_EXECUTION,
                        SERIAL_EXECUTE, MASTER_TIMER, GPIO_LIST)


def get_timer(tim_id):
    ''' instantiate and returns instance of the timer, specified
    by tim_id

    args:
        tim_id: string describing timer to use:
        - "TIM1" or "tim1" to specify first TIM1
        - "PA0" or "pa0" to select timer, generating signal on PA0
        - "D9" or "d9" to select timer, generating on ping D9
                                        (in arduino notation)
    '''
    try:
        assert isinstance(tim_id, str)
        if tim_id[:3].lower() == "tim":
            id = int(tim_id[3:])
            idx = [key for (key, val) in pin_mapping['tim'].items()
                   if val == id]
        else:
            for typ in ['pin', 'port']:
                idx = [key for (key, val) in pin_mapping[typ].items()
                       if val == tim_id.lower()]
                if idx:
                    break
        idx = idx[0]
    except Exception as e:
        print(e)
        raise ValueError("""Cant find corresponding timer. Please provide timer id as
            tim1 for TIM1 or d5 for pin 5 or pa5 for port PA5""")

    channel = pin_mapping['chan'][idx]
    port = pin_mapping['port'][idx]
    pin = pin_mapping['pin'][idx]
    name = f"TIM{pin_mapping['tim'][idx]}"
    sync = pin_mapping['sync'][idx]
    print(f"Found timer {name}, pin: {pin}, port: {port}")
    if name == MASTER_TIMER:
        warnings.warn("""Selected master timer! All other timers will start
            simulaneously! Do not use timer.on_sync() in that case.""")
    tim = Timer(default_channel=channel,
                hw_desc=hw_desc[name],
                name=name,
                synchronizable=sync)
    return tim


def get_gpio(gpio_id):
    ''' instantiate and returns instance of GPIO, specified
    by gpio_id

    args:
        gpio_id: string describing GPIO to use:
        - "GPIOA" to specify GPIOA.
    '''
    assert isinstance(gpio_id, str)
    if gpio_id.upper() in GPIO_LIST:
        gpio_id = gpio_id.upper()
    else:
        raise ValueError(f"Can't find that GPIO, existing are {GPIO_LIST}")
    print(f"Found {gpio_id}")
    gpio = GPIO(hw_desc=hw_desc[gpio_id],
                name=gpio_id)
    return gpio


def start_execution(ser):
    ''' Start actual execution of the program
    by sending START_EXECUTION byte to microcontroller
    '''
    ser.write(SERIAL_EXECUTE)
    # return ser.read_until()


def stop_execution(ser):
    ser.write(SERIAL_STOP_EXECUTION)


def send_program(ser, prog):
    ''' send the generated program to microntroller '''
    crc = zlib.crc32(prog).to_bytes(4, byteorder="little")
    packet = SERIAL_START + prog + crc + SERIAL_END
    ser.write(packet)
    return ser.read_until()

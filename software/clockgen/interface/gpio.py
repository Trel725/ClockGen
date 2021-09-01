from collections import Iterable

from .base_interface import BaseInterface
from ..utils import get_gpio
from .. import pin_mapping


class GPIO(BaseInterface):
    """
    Interface for controlling GPIO of microntroller.
    """

    def __init__(self, id):
        ''' instantiate given GPIO
        args:
            id - id of gpio, e.g. GPIOA
        '''
        super(GPIO, self).__init__()
        self.gpio = get_gpio(id)
        self.hw = [self.gpio]
        self.tim_pins = list(pin_mapping['port'].values())

    def _val_pins(self, pins):
        port_letter = self.gpio.name[-1].lower()
        for pin in pins:
            if f"p{port_letter}{pin}" in self.tim_pins:
                raise ValueError(
                    f"Can't use p{port_letter}{pin} as GPIO, its in use by timer!")

    def on(self, pins, time):
        ''' switch given pins to HIGH at specified time
        args:
            pins: pin or list of pins to turn on
            time: time at which to turn these pins on
        '''
        if not isinstance(pins, Iterable):
            pins = [pins]
        self._val_pins(pins)
        [self.gpio.on(pin) for pin in pins]
        self.add_frame(time)

    def off(self, pins, time):
        ''' switch given pins to LOW at specified time
        args:
            pins: pin or list of pins to turn off
            time: time at which to turn these pins off
        '''
        if not isinstance(pins, Iterable):
            pins = [pins]
        [self.gpio.off(pin) for pin in pins]
        self.add_frame(time)

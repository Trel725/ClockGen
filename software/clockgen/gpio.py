from . import Periph


class GPIO(Periph):
    """docstring for GPIO"""

    def __init__(self, *args, **kwargs):
        super(GPIO, self).__init__(*args, **kwargs)

    def on(self, pin):
        self.ODR.set_bit(pin)

    def off(self, pin):
        self.ODR.reset_bit(pin)

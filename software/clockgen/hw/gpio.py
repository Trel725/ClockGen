from . import Periph


class GPIO(Periph):
    """Class, providing basic GPIO functionality
    by manipulating bits in corrseponding registers."""

    def __init__(self, *args, **kwargs):
        '''
        Instantiate this class as:
        gp = GPIO(hw_desc=hw_desc['GPIOA'],
                    name="GPIOA")
         args:
            hw_desc: hardware description for given timer,
            available as hw_desc['TIMx'],
            name: name of the timer, any string that makes sense

        typical usage, enable and disable of pin 7:
            gp.on(7)
            gp.off(7)

        '''
        super(GPIO, self).__init__(*args, **kwargs)

    def on(self, pin):
        self.ODR.set_bit(pin)

    def off(self, pin):
        self.ODR.reset_bit(pin)

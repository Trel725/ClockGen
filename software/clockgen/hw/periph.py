from . import Register


class Periph(object):
    """Base class for microcontroller peripherals
    Use like: gpio = Periph(hw_desc['GPIOA'], name="GPIOA")
    Exports all registers of given peripheral as class atrributes,
    thus allows convinient access like gpio.ODR, gpio.OTYPER, etc
    """

    def __init__(self, hw_desc, name):
        super(Periph, self).__init__()
        self.name = name
        self.registers = hw_desc
        regs = {}
        # export registers as class attributes
        for regname, regdata in self.registers.items():
            reg = Register(regdata)
            setattr(self, regname, reg)
            regs[regname] = reg
        self.registers = regs

    def get_modified_regs(self, update=True):
        '''return list of registers, which values have changed
        from previous call of this method (if update=True) or
        from reset (if update=False).
        If you want to force register update,
        set its _prev_value to -1
        '''
        regs = [reg for reg in self.registers.values()
                if reg.value != reg._prev_value]
        if update:
            for r in regs:
                r._prev_value = r.value
        return regs

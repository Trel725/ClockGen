from . import Register


class Periph(object):
    """Base class for uC peripherals"""

    def __init__(self, hw_desc, name):
        super(Periph, self).__init__()
        self.name = name
        self.registers = hw_desc
        regs = {}
        for regname, regdata in self.registers.items():
            reg = Register(regdata)
            setattr(self, regname, reg)
            regs[regname] = reg
        self.registers = regs

    def get_modified_regs(self, update=True):
        '''returns list of changed registers from reset (if update=False)
            or from previous call (if update=True)
          #registers with prev_value == -1 are always updated,
          #which is useful for dynamic registers (e.g. counter)
          above two lines are not true
        '''
        regs = [reg for reg in self.registers.values()
                if reg.value != reg._prev_value]
        if update:
            for r in regs:
                # if r._prev_value >= 0:
                r._prev_value = r.value
        return regs

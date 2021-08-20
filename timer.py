import json


class Register(object):
    '''
    Class, holding description for low-level C-like registers,
    described by desc (generated from SVD file)

        main usage:
        1. create instance
        gpioa = Register(hw_desc['GPIOA']['ODR'])
        2. use set_field to set bit values. This function supports
        both setting and resetting, i.e.
        gpioa.set_field(gpioa.ODR10, 1)
        gpioa.set_field(gpioa.ODR10, 0)

    '''

    def __init__(self, desc):
        self.desc = desc
        for key in desc:
            setattr(self, key, desc[key])

        for field in desc['fields']:
            setattr(self, field, desc['fields'][field])

        self._value = self.reset_value
        self._prev_value = self.reset_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if val > (2**self.size) - 1:
            raise ValueError(
                f"Cant set val {val} to register having {self.size} bits")
        self._value = val

    def __repr__(self):
        tmp = dict(self.desc)
        del tmp['fields']
        c = "Instance of class Register:\n"
        return c + "{" + "\n".join("{!r}: {!r},"
                                   .format(k, v) for k, v in tmp.items()) + "}"

    def validate(self, offset, bit_width):
        assert offset + bit_width < self.size, \
            "Trying to set bits off register"
        assert "write" in self.access, \
            "Trying to modify read-only register"
        assert ((((2**bit_width) - 1) << offset) & (~self.reset_mask)) == 0, \
            "Trying to set bits on read-only positions"

    def set_bit(self, offset):
        self.validate(offset, 1)
        self.value = self.value | (1 << offset)

    def reset_bit(self, offset):
        self.validate(offset, 1)
        self.value = self.value & ~(1 << offset)

    def set_bits(self, offset, bit_width, value):
        self.validate(offset, bit_width)
        self.value = self.value | (value << offset)

    def reset_bits(self, offset, bit_width):
        self.validate(offset, bit_width)
        self.value = self.value & ~(((2**bit_width) - 1) << offset)

    def set_field(self, field, value):
        offset = field['bit_offset']
        width = field['bit_width']
        self.reset_bits(offset, width)
        self.set_bits(offset, width, value)

    def reset_value(self):
        self.value = self.reset_value


class Periph(object):
    """Base class for uC peripherals"""

    def __init__(self, name, hw_desc):
        super(Periph, self).__init__()
        # with open(hw_desc, "r") as f:
        #    self.hw_desc = json.load(f)
        self.hw_desc = hw_desc
        self.name = name
        self.registers = hw_desc[name]
        regs = {}
        for regname, regdata in self.registers.items():
            reg = Register(regdata)
            setattr(self, regname, reg)
            regs[regname] = reg
        self.registers = regs

    def get_modified_regs(self, update=True):
        '''returns list of changed registers from reset (if update=False)
            or from previous call (if update=True)
          registers with prev_value == -1 are always updated,
          which is useful for dynamic registers (e.g. cnter)
        '''
        regs = [reg for reg in self.registers.values()
                if reg.value != reg._prev_value]
        if update:
            for r in regs:
                if r._prev_value >= 0:
                    r._prev_value = r.value
        return regs


class Timer(Periph):
    """docstring for Timer"""

    def __init__(self, *args, **kwargs):
        super(Timer, self).__init__(*args, **kwargs)
        # do not update prev_value for CNT,
        # instead set it each time its requested
        self.CNT._prev_value = -1
        self.CCMR1_Output._prev_value = -1
        self.CCMR2_Output._prev_value = -1

    def toggle_channel(self, channel, value):
        """
        must set TIM->CCER->CC1E to enable first channel, and so on
        """
        try:
            self.CCER.set_field(self.CCER.fields[f'CC{channel}E'], value)
        except KeyError:
            print(f"Timer does not have this channel: {channel}")

    def toggle_polarity(self, channel, value):
        '''
        bit TIM->CCER->CC1P controls polarity of first channel
        value 0 -> active high
        value 1 -> active low'''
        try:
            self.CCER.set_field(self.CCER.fields[f'CC{channel}P'], value)
        except KeyError:
            raise ValueError(f"Timer does not have this channel: {channel}")

    def set_autoreload(self, value):
        '''
        value at which counter will
        automaticlly reload and generate GPIO toggle
        TIM->ARR'''
        self.ARR.value = value

    def set_counter(self, value):
        # TIM->CNT - current value of a counter
        self.CNT.value = value

    def start(self):
        # need to set TIM->CR1->CEN to enable counter
        self.CR1.set_field(self.CR1.CEN, 1)

    def stop(self):
        # need to reset TIM->CR1->CEN to disable counter
        self.CR1.set_field(self.CR1.CEN, 0)


class GPIO(Periph):
    """docstring for GPIO"""

    def __init__(self, *args, **kwargs):
        super(Timer, self).__init__(*args, **kwargs)


class ProgramGen(object):
    """docstring for ProgramGen"""

    def __init__(self):
        super(ProgramGen, self).__init__()
        self.frames = []

        # end of frame
        self.eof = 0xABBCCDDE
        # end of programm
        self.eop = 0xFFFFFFFF

    @staticmethod
    def _flatten_cmds(cmds):
        return [elem for iterable in cmds for elem in iterable[1:]]

    @staticmethod
    def _binarize(vals):
        data_bin = b"".join([item.to_bytes(4, byteorder="little")
                             for item in vals])
        return data_bin

    def print_program(self):
        for frame in self.frames:
            print(f"@ {frame['time']}")
            for name, addr, val in frame['cmds']:
                print(f"    {name:<15}:{hex(addr)}:{hex(val)}")

    def add_frame(self, hws, time):
        cmds = []
        for hw in hws:
            regs = hw.get_modified_regs()
            cmds.extend([(f"{hw.name}->{r.name}", r.address, r.value)
                         for r in regs])

        self.frames.append(dict(time=time,
                                cmds=cmds))

    def generate_program(self):
        prg = []
        for frame in self.frames:
            prg.append(frame['time'])
            prg.extend(self._flatten_cmds(frame['cmds']))
            prg.append(self.eof)
        prg.append(self.eop)
        return self._binarize(prg)

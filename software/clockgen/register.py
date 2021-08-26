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
        return c + "{" + "\n".join("    {!r}: {!r},"
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

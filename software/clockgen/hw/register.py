class Register(object):
    '''
    Class, holding description for low-level C-like registers,
    described by desc (generated from SVD file)
    '''

    def __init__(self, desc):
        ''' Typical usage:
            1. create instance
            gpioa = Register(hw_desc['GPIOA']['ODR'])
            2. use set_field to set bit values. This method supports
            both setting and resetting, i.e.
            gpioa.set_field(gpioa.ODR10, 1)
            gpioa.set_field(gpioa.ODR10, 0)
        '''
        self.desc = desc
        # register properties are appended
        # as class attributes. Allows usage
        # of expression like self.size and
        # exports register field names, like self.CEN
        # to refer to CEN field in CR1 register
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
        fields = tmp['fields']
        del tmp['fields']
        s = "Instance of class Register:\n"
        s += f"current value: {bin(self.value)}\n"

        s += "\n".join("    {!r}: {!r},"
                       .format(k, v) for k, v in tmp.items()) + "\n"

        s += "Fields:\n"
        for name, val in fields.items():
            s += f"  {name}\n"
            s += "\n".join("        {!r}: {!r},"
                           .format(k, v) for k, v in val.items()) + "\n"
        return s

    def validate(self, offset, bit_width):
        assert offset + bit_width < self.size, \
            "Trying to set bits off register"
        assert "write" in self.access, \
            "Trying to modify read-only register"
        assert ((((2**bit_width) - 1) << offset) & (~self.reset_mask)) == 0, \
            "Trying to set bits on read-only positions"

    def set_bit(self, offset):
        """
        Set single bit in register at offset
        """
        self.validate(offset, 1)
        self.value = self.value | (1 << offset)

    def reset_bit(self, offset):
        """
        Reset single bit in register at offset
        """
        self.validate(offset, 1)
        self.value = self.value & ~(1 << offset)

    def set_bits(self, offset, bit_width, value):
        """
        Set multiple bits in register at offset.
        Note: this method will only set bits, i.e.
        even if value=0b101 the central bit is not
        guaranteed to be zero, this reset_bits is
        recommended before calling this methos
        """
        self.validate(offset, bit_width)
        self.value = self.value | (value << offset)

    def reset_bits(self, offset, bit_width):
        """
        Reset multiple bits from offset to offset+bit_width
        e.g. for offset=2, bit_width=2
        0b1111_1111 -> 0b1111_0011
        """
        self.validate(offset, bit_width)
        self.value = self.value & ~(((2**bit_width) - 1) << offset)

    def set_field(self, field, value):
        """
        Assigns corresponding value to given field.
        Fields are available as self.FIELD, e.g. self.CEN
        In other words, use this method as:
        reg.set_field(reg.OTYPER5, 1)
        """
        offset = field['bit_offset']
        width = field['bit_width']
        self.reset_bits(offset, width)
        self.set_bits(offset, width, value)

    def reset_value(self):
        '''
        Reset value of register to its
        reset value, i.e. simulates chip reset
        '''
        self.value = self.reset_value

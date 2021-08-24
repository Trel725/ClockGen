
class BaseInterface(object):
    """docstring for BaseInterface"""

    def __init__(self):
        super(BaseInterface, self).__init__()
        self.frames = []
        self._hw = None

    @property
    def hw(self):
        if self._hw is not None:
            return self._hw
        else:
            raise ValueError("self.hw is not set!")

    @hw.setter
    def hw(self, hw):
        self._hw = hw

    def print_program(self):
        for frame in self.frames:
            print(f"@ {frame['time']}")
            for name, addr, val in frame['cmds']:
                print(f"    {name:<20}:{hex(addr)}:{hex(val)}")

    def add_frame(self, time):
        cmds = []
        for hw in self.hw:
            regs = hw.get_modified_regs()
            cmds.extend([(f"{hw.name}->{r.name}", r.address, r.value)
                         for r in regs])

        self.frames.append(dict(time=time,
                                cmds=cmds))

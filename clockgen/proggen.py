import copy

from .constants import EOF, EOP


class ProgramGen(object):
    """docstring for ProgramGen"""

    def __init__(self):
        super(ProgramGen, self).__init__()
        self.frames = []
        self.opt_frames = []

    @staticmethod
    def _flatten_cmds(cmds):
        return [elem for iterable in cmds for elem in iterable[1:]]

    @staticmethod
    def _binarize(vals):
        data_bin = b"".join([item.to_bytes(4, byteorder="little")
                             for item in vals])
        return data_bin

    def print_program(self):
        for frame in self.opt_frames:
            print(f"@ {frame['time']}")
            for name, addr, val in frame['cmds']:
                print(f"    {name:<20}:{hex(addr)}:{hex(val)}")

    @staticmethod
    def combine_by_time(frames):
        out_frames = []
        for fr in frames:
            if not out_frames:
                out_frames.append(fr)
                continue
            if fr['time'] == out_frames[-1]['time']:
                out_frames[-1]['cmds'].extend(fr['cmds'])
                continue
            out_frames.append(fr)
        return out_frames

    def optimize(self, frames):
        frames = sorted(frames, key=lambda x: x['time'])
        return self.combine_by_time(frames)

    def generate_program(self, hw_list):
        self.frames = [copy.deepcopy(frame)
                       for hw in hw_list for frame in hw.frames]
        self.opt_frames = self.optimize(self.frames)
        return self.binarize_program(self.opt_frames)

    def binarize_program(self, frames):
        prg = []
        for frame in frames:
            prg.append(frame['time'])
            prg.extend(self._flatten_cmds(frame['cmds']))
            prg.append(EOF)
        prg.append(EOP)
        return self._binarize(prg)

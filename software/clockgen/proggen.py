import copy

from .constants import EOF, EOP, MIN_START_TIME


class ProgramGen(object):
    """Program generator for microntroller. Provides
    methods to generate program from list of hardware
    """

    def __init__(self):
        super(ProgramGen, self).__init__()
        self.frames = []
        self.opt_frames = []

    @staticmethod
    def _flatten_cmds(cmds):
        ''' return flat list of commands from '''
        return [elem for iterable in cmds for elem in iterable[1:]]

    @staticmethod
    def _binarize(vals):
        '''convert input list to little-ended binary'''
        data_bin = b"".join([item.to_bytes(4, byteorder="little")
                             for item in vals])
        return data_bin

    def print_program(self):
        '''visualize the generated program'''
        for frame in self.opt_frames:
            print(f"@ {frame['time']}")
            for name, addr, val in frame['cmds']:
                print(f"    {name:<20}:{hex(addr)}:{hex(val)}")

    def get_prog_dict(self):
        return self.opt_frames

    def set_prog_dict(self, frames):
        self.opt_frames = frames

    @staticmethod
    def combine_by_time(frames):
        ''' simple optimization pass that
        combines together frames, which
        should be executed at the same time
        '''
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

    @staticmethod
    def normalize_time(frames):
        min_time = min([fr['time'] for fr in frames])
        for fr in frames:
            fr['time'] -= min_time
            fr['time'] += MIN_START_TIME
        return frames

    def optimize(self, frames):
        ''' performs program optimization '''
        frames = sorted(frames, key=lambda x: x['time'])
        frames = self.combine_by_time(frames)
        frames = self.normalize_time(frames)
        return frames

    def generate_program(self, hw_list):
        ''' Generate complete binary program from list of hardware
        args:
            hw_list - list of instances of classes, inherited from BaseInterfase
        '''
        self.frames = [copy.deepcopy(frame)
                       for hw in hw_list for frame in hw.frames]
        self.opt_frames = self.optimize(self.frames)
        return self.binarize_program(self.opt_frames)

    def binarize_program(self, frames):
        ''' Build binary program by wrapping each frame in the format:
        time_stamp - commands to execute - END OF FRAME
        and binarizing sequence of such frames'''
        prg = []
        for frame in frames:
            prg.append(frame['time'])
            prg.extend(self._flatten_cmds(frame['cmds']))
            prg.append(EOF)
        prg.append(EOP)
        return self._binarize(prg)

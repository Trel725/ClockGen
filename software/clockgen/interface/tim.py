import warnings

from .base_interface import BaseInterface

from ..constants import TIM_FREQ
from ..constants import TIM_INIT_DELAY
from ..utils import get_timer
from .. import master_timer


class TIM(BaseInterface):
    """A high-level interface for timer.
    This class implements interface for generating
    signals with timer"""

    def __init__(self, id):
        '''
        instantiate given timer
        args:
            id - timer index or port corresponding to the timer
        '''
        super(TIM, self).__init__()
        self.timer = get_timer(id)
        self.hw = [master_timer]
        self.hw.append(self.timer)
        # maximum time of command so far
        # needed to prevent setting time in past
        self.max_time = -1
        # whether timer have been started in synced manner
        self.synced = False

    def _prestart(self, arr, time):
        '''initializes timer, by adding
        initialization commands to program
        at time - TIM_INIT_DELAY '''
        # we need to initialize timer before start
        # the timer might be running, stop it
        self.timer.stop()
        # set its frequency
        self.timer.set_autoreload(arr)
        # set countner value to prevent sudden out pin toggling
        self.timer.set_counter(arr)
        # enable toggle on timer overload, want square wave
        self.timer.force_out_toggle()
        # enable output channel
        self.timer.set_out_channel_mode(self.timer.default_channel, 1)
        self.add_frame(time - TIM_INIT_DELAY)

    def _poststop(self):
        ''' deinitializes timer'''
        # force low level on output channel
        self.timer.force_out_low()
        # disable output channel
        self.timer.set_out_channel_mode(self.timer.default_channel, 0)

    def _val_time(self, time):
        if time < self.max_time:
            raise ValueError(
                "Time of operation can't be less than time of previous one")

    def _val_sync(self):
        if not self.timer.synchronizable:
            raise ValueError(
                "This timer is not synchronizable! Use normal on/off or another timer")

    def on(self, freq, time):
        '''
        Start the timer, begin generating square wave at
        specified time.
        args:
            freq - frequency of the generated signal
            time - time to start generation (first low->high transition)
        '''
        self._val_time(time)
        arr = (TIM_FREQ // (2 * freq)) - 1
        real_freq = TIM_FREQ / (2 * (arr + 1))
        if real_freq != freq:
            warnings.warn(f"Timer can't tick at desrired frequency! \
                You will get instead {real_freq} Hz")
        self._prestart(arr, time)
        self.timer.start()
        self.add_frame(time)

    def change_freq(self, freq, time):
        '''
        Change timer frequncy on-the-fly at specified time.
        Note that changing of frequency might lead to losing
        sychronization.

        args:
            freq - frequency of the generated signal
            time - time at which frequency will be changed
        TODO: is multiple of the frequency safe? ARR preload?
        '''
        self._val_time(time)
        arr = (TIM_FREQ // (2 * freq)) - 1
        real_freq = TIM_FREQ / (2 * (arr + 1))
        if real_freq != freq:
            warnings.warn(f"Timer can't tick at desrired frequency! \
                You will get instead {real_freq} Hz")
        self.timer.set_autoreload(arr)
        self.add_frame(time)

    def on_sync(self, freq, time):
        '''
        Prepare to start the timer, begin generating square wave at
        specified time. This method does not actually start timer but
        only performs preparations. Actual start is done by calling
        tim.start_sync(), which enables all initialized timers
        simultaniously.

        args:
            freq - frequency of the generated signal
            time - time to perform initialization. Normally few cycles before
            actual start.

        '''
        if self.timer.name == master_timer.name:
            raise ValueError(
                "Don't use on_sync on master timer! Simple on() will turn all the timers synchroneously!")
        self._val_sync()
        self.synced = True
        self._val_time(time)
        arr = (TIM_FREQ // (2 * freq)) - 1
        real_freq = TIM_FREQ / (2 * (arr + 1))
        if real_freq != freq:
            warnings.warn(f"Timer can't tick at desrired frequency! \
                You will get instead {real_freq} Hz")
        self._prestart(arr, time)

    def start_sync(self, time):
        ''' Starts all the initialized timers at specified time
        by starting master timer. Thus, this function need to be called
        on just one instance of timer, all other will start automatically.

        args:
            time - time to start generation (first low->high transition)
        '''
        self._val_sync()
        master_timer.start()
        self.add_frame(time)
        master_timer.stop()
        self.add_frame(time + 1)

    def off(self, time):
        ''' stop the running timer
        
        args:
            time - time at which timer will stop
        '''
        if self.synced:
            raise ValueError(
                "Timer have been started in sync mode! Use off_sync()")
        self._val_time(time)
        self.timer.stop()
        self._poststop()
        self.add_frame(time)

    def off_sync(self, time):
        ''' stop the running timer, that have been turned on synchronously.
        
        args:
            time - time at which timer will stop
        '''
        self._val_sync()
        if not self.synced:
            raise ValueError(
                "Timer have not been started in sync mode! Use off()")
        self._val_time(time)
        self.timer.CR1._prev_value = -1
        self.timer.stop()
        self._poststop()
        self.add_frame(time)

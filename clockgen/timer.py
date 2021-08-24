from . import Periph

FORCE_LOW = 4
TOGGLE = 3


class Timer(Periph):
    """docstring for Timer"""

    def __init__(self, default_channel=1,
                 synchronizable=False,
                 *args, **kwargs):
        super(Timer, self).__init__(*args, **kwargs)
        self.default_channel = default_channel
        self.synchronizable = synchronizable

    def set_out_channel_mode(self, channel, value):
        """
        must set TIM->CCER->CC1E to enable first channel, and so on
        """
        try:
            self.CCER.set_field(self.CCER.fields[f'CC{channel}E'], value)
        except KeyError:
            print(f"Timer does not have this channel: {channel}")

    def set_polarity(self, channel, value):
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

    def set_counter(self, value, force=True):
        # TIM->CNT - current value of a counter
        self.CNT.value = value
        # do not update prev_value for CNT,
        # instead set it each time its requested
        self.CNT._prev_value = -1

    def start(self):
        # need to set TIM->CR1->CEN to enable counter
        self.CR1._prev_value = -1
        self.CR1.set_field(self.CR1.CEN, 1)

    def stop(self):
        # need to reset TIM->CR1->CEN to disable counter
        self.CR1._prev_value = -1
        self.CR1.set_field(self.CR1.CEN, 0)

    def force_out_low(self):
        # force output to be in low mode even if timer stopped
        # while output is in high mode
        if self.default_channel in [1, 2]:
            self.CCMR1_Output.set_field(
                self.CCMR1_Output.fields[f'OC{self.default_channel}M'],
                FORCE_LOW)

        if self.default_channel in [3, 4]:
            self.CCMR2_Output.set_field(
                self.CCMR2_Output.fields[f'OC{self.default_channel}M'],
                FORCE_LOW)

    def force_out_toggle(self):
        # force output to be in TOGGLE
        if self.default_channel in [1, 2]:
            self.CCMR1_Output.set_field(
                self.CCMR1_Output.fields[f'OC{self.default_channel}M'],
                TOGGLE)

        if self.default_channel in [3, 4]:
            self.CCMR2_Output.set_field(
                self.CCMR2_Output.fields[f'OC{self.default_channel}M'],
                TOGGLE)

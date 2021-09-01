from . import Periph

FORCE_LOW = 4
TOGGLE = 3


class Timer(Periph):
    """Class, providing basic timer functionality
    by manipulating bits in corrseponding registers.
    """

    def __init__(self, default_channel=1,
                 synchronizable=False,
                 *args, **kwargs):
        '''
        Instantiate this class as:
        tim = Timer(hw_desc=hw_desc['TIM2'],
                    name="TIM2",
                    default_channel=2,
                    synchronizable=True,
                    )
        args:
            hw_desc: hardware description for given timer,
            available as hw_desc['TIMx'],
            name: name of the timer, any string that makes sense
            default_channel: channel at which timer will generate output
            synchronizable: whether start of MASTER_TIMER will start this
            timer too
        '''
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
        value 0: active high
        value 1: active low'''
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
        '''
        set counter value
        TIM->CNT
        '''
        self.CNT.value = value
        # do not update prev_value for CNT,
        # instead set it each time its requested
        self.CNT._prev_value = -1

    def start(self):
        '''
        need to set TIM->CR1->CEN to enable counter
        '''
        self.CR1.set_field(self.CR1.CEN, 1)
        # force setting of the corresponding value
        # each time its requested:
        self.CR1._prev_value = -1

    def stop(self):
        '''
        need to reset TIM->CR1->CEN to disable counter
        '''
        self.CR1.set_field(self.CR1.CEN, 0)
        # force setting of the corresponding value
        # each time its requested:
        self.CR1._prev_value = -1

    def force_out_low(self):
        """
        force output to be LOW even if timer was
        stopped while with its output was HIGH.
        To do this its necessary to change mode of
        output channel (CCMR1_Output->OC2M) into FORCE_LOW"""
        if self.default_channel in [1, 2]:
            self.CCMR1_Output.set_field(
                self.CCMR1_Output.fields[f'OC{self.default_channel}M'],
                FORCE_LOW)

        if self.default_channel in [3, 4]:
            self.CCMR2_Output.set_field(
                self.CCMR2_Output.fields[f'OC{self.default_channel}M'],
                FORCE_LOW)

    def force_out_toggle(self):
        """
        Restore normal behavious of timer output
        (toggle on counter overload).
        To do this its necessary to change mode of
        output channel (CCMR1_Output->OC2M) into TOGGLE"""
        if self.default_channel in [1, 2]:
            self.CCMR1_Output.set_field(
                self.CCMR1_Output.fields[f'OC{self.default_channel}M'],
                TOGGLE)

        if self.default_channel in [3, 4]:
            self.CCMR2_Output.set_field(
                self.CCMR2_Output.fields[f'OC{self.default_channel}M'],
                TOGGLE)

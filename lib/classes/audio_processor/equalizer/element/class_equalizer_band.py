# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Equalizer : Band
#
#   Band of an Equalizer
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.audio_processor.equalizer.element.class_equalizer_band_bandwidth import \
    EqualizerBandBandwidth
from lib.classes.audio_processor.equalizer.element.class_equalizer_band_frequency import \
    EqualizerBandFrequency
from lib.classes.audio_processor.equalizer.element.class_equalizer_band_gain import \
    EqualizerBandGain

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class EqualizerBand():
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, equalizer, index):

        # store sttribuates
        self.equalizer = equalizer

        # index
        self.index = index

        # sfz tag
        self.tag = "eq" + str(self.index)

        # setup attributes
        self.frequency = EqualizerBandFrequency(self.equalizer)
        self.gain = EqualizerBandGain(self.equalizer)
        self.bandwidth = EqualizerBandBandwidth(self.equalizer)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        # return string
        data = ""

        # add depth data
        data += self.tag + "_" + self.frequency.tag + "=" + str(self.frequency.depth + self.frequency.calculate_compensation()) + "\n"
        data += self.tag + "_" + self.gain.tag + "=" + str(self.gain.depth + self.gain.calculate_compensation()) + "\n"
        data += self.tag + "_" + self.bandwidth.tag + "=" + str(self.bandwidth.depth + self.bandwidth.calculate_compensation()) + "\n"

        # get modulation lines
        freq_mod_lines = self.frequency.get_modulation()
        gain_mod_lines = self.gain.get_modulation()
        bw_mod_lines = self.bandwidth.get_modulation()

        # add modulation frequency sfz
        for line in freq_mod_lines:
            data += self.tag + "_" + line + "\n"

        # add modulation gain sfz
        for line in gain_mod_lines:
            data += self.tag + "_" + line + "\n"

        # add modulation bandwidth sfz
        for line in bw_mod_lines:
            data += self.tag + "_" + line + "\n"

        # return sfz string
        return data

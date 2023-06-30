# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : LFO : Waveform
#
#   Represents a modulatable value of a LFO
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.lfo.values.class_lfo_value import LfoValue
from lib import lookup

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class LfoWaveform(LfoValue):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, lfo):

        # super constructor
        super().__init__(instrument, lfo)

        # default to sine
        self.depth = 1

        # sfz tag
        self.tag = self.lfo.tag + "_wave"

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Waveform
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_waveform(self, wave):

        # load wave by using the string if one is given
        if type(wave) is str:

            # try loading waveform from string
            try:
                self.depth = lookup.LFO_WAVEFORM[wave]
            except:
                pass

        else:
            # set straight number if argument is one
            self.depth = wave

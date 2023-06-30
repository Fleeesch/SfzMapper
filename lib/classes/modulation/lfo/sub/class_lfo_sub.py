# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : LFO : Sub
#
#   Custom LFO covered by the SFZ2 Standard
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class LfoSub():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, lfo):

        # lfo reference
        self.lfo = lfo
        
        # lfo reference
        self.index = len(self.lfo.sub_lfo) + 2
        
        # default attributes
        self.wave = self.lfo.waveform.depth
        self.ratio = 1
        self.scale = 1
        self.offset = 0

        # add to lfo lookup
        self.lfo.sub_lfo.append(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        data = ""

        # waveform
        data += self.lfo.tag + "_wave" + str(self.index) + "=" + str(self.wave) + "\n"
        
        # ratio
        data += self.lfo.tag + "_ratio" + str(self.index) + "=" + str(self.ratio) + "\n"
        
        # scale
        data += self.lfo.tag + "_scale" + str(self.index) + "=" + str(self.scale) + "\n"
        
        # offset
        data += self.lfo.tag + "_offset" + str(self.index) + "=" + str(self.offset) + "\n"
        
        return data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Pitchbend
#
#   Stores Pitchbend setting data,
#   ready to be printed for a SFZ file
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Pitchbend():
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, source, range=12, step=0, smooth=0):
        
        # store relations
        self.source = source
        self.instrument = source.instrument
        
        # smoothing
        self.smooth = smooth
        
        # assume range is single value
        self.range_up = range
        self.range_down = -range
        
        # assume step is single value
        self.step_up = step
        self.step_down = -step
        
        # store separate range values if given
        if type(range) is list:
            self.range_up = range[0]
            self.range_down = range[1]
        
        # store separate step values if given
        if type(step) is list:
            self.step_up = step[0]
            self.step_down = abs(step[1])
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz(self):
        
        data = ""
        
        # add smoothing if not 0
        if self.smooth:
            data += "bend_smooth=" + str(self.smooth) + "\n"
        
        # range
        data += "bend_up=" + str(self.range_up) + "\n"
        data += "bend_down=" + str(self.range_down) + "\n"
        
        # add step if not 0
        if self.step_up:
            data += "bend_stepup=" + str(self.step_up) + "\n"
        if self.step_down:
            data += "bend_stepdown=" + str(self.step_down) + "\n"

        return data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Range : CC Trigger
#
#   Control Change range used for
#   triggering playback
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_range import Range

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class RangeCCTrigger(Range):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, source, control):
        
        super().__init__()
        
        # store references
        self.source = source
        self.instrument = self.source.instrument
        
        # control reference
        self.control = control
        
        # store range in structure lookup table
        self.source.range_cc_trigger.append(self)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Attribute
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz(self):
        
        data = ""
        
        # skip if range covers the whole spectrum (default setting)
        if self.range_low == 0 and self.range_high == 127:
            return ""
        
        # use range for keyswitch
        data += "on_locc" + str(self.control.cc) + "=" + str(self.range_low) + "\n"
        data += "on_hicc" + str(self.control.cc) + "=" + str(self.range_high) + "\n"
        
        # return sfz string
        return data

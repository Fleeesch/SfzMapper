# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Range : CC HD
#
#   Control Change range used for
#   context control of regions
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .class_range_cc import RangeCC

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class RangeCCHD(RangeCC):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, source, control):
        
        super().__init__(source, control)
        
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Attribute
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz(self):
        
        data = ""
        
        # skip if range covers the whole spectrum (default setting)
        if self.range_low == 0 and self.range_high == 127:
            return ""
        
        # use range for keyswitch
        data += "lohdcc" + str(self.control.cc) + "=" + str(self.range_low) + "\n"
        data += "hihdcc" + str(self.control.cc) + "=" + str(self.range_high) + "\n"

        # return sfz string
        return data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Equalizer : Band : Frequency
#
#   Frequency Attribute of an Equalizer Band
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.modulators import class_modulation_cc as mod_cc
from lib.classes.sfz_structure.attributes.class_attribute import Attribute

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class EqualizerBandFrequency(Attribute):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, equalizer, depth=3000):
        
        # super constructor
        super().__init__(equalizer.instrument)
        
        # store sttribuates
        self.equalizer = equalizer
        self.depth = depth
        
        # sfz tag
        self.tag = "freq"
        
        # modulation candidates
        self.set_modulation_candidates(mod_cc.ModulationCC)

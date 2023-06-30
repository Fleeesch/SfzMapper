# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Filter : Type : High-Pass
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.audio_processor.filter.type.class_filter_type import FilterType
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FilterTypeHighpass(FilterType):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, filter):
        
        # super constructor
        super().__init__(filter)
        
        # available poles
        self.poles_lookup = [1, 2, 4, 6]
        
        # sfz tag
        self.tag = "hpf"

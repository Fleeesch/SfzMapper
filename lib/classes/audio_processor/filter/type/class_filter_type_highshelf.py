# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Filter : Type : High-Shelf
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.audio_processor.filter.type.class_filter_type import FilterType
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FilterTypeHighShelf(FilterType):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, filter):
        
        # super constructor
        super().__init__(filter)
        
        # available poles
        self.poles_lookup = None
        
        # sfz tag
        self.tag = "hsh"

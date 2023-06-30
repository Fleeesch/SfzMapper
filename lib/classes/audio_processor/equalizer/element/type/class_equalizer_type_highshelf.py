# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# =============================================================
#   Class : Audio Processor : Equalizer : Type : High-Shelf
# =============================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.audio_processor.equalizer.element.type.class_equalizer_type import EqualizerType

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class EqualizerTypeHighShelf(EqualizerType):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, equalizer):
        
        # super constructor
        super().__init__(equalizer)
        
        # sfz tag
        self.tag = "hshelf"

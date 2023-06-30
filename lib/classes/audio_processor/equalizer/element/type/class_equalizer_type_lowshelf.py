# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# =============================================================
#   Class : Audio Processor : Equalizer : Type : Low-Shelf
# =============================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.audio_processor.equalizer.element.type.class_equalizer_type import EqualizerType

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class EqualizerTypeLowShelf(EqualizerType):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, equalizer):
        
        # super constructor
        super().__init__(equalizer)
        
        # sfz tag
        self.tag = "lshelf"

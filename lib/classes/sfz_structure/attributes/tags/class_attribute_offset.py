# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulatable : Attribute : Offset
#
#   Offset Attribute
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_attribute import Attribute

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class AttributeOffset(Attribute):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, level):

        # super constructor
        super().__init__(instrument)

        # default settings
        self.level = level

        # sfz tag
        self.tag = "offset"

        self.skip_smooth = True
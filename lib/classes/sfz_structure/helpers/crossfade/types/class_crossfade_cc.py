# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Crossfade : CC
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from lib.classes.sfz_structure.helpers.crossfade.class_crossfade import \
    Crossfade

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class CrossfadeCC(Crossfade):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, type, depth, index=0):

        # super constructor
        super().__init__(type, depth)

        # tags
        self.tag_range = "cc" + str(index)
        self.tag_curve = "xf_cccurve"

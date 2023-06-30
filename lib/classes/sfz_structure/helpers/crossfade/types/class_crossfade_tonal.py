# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Crossfade : Tonal
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


class CrossfadeTonal(Crossfade):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, type, depth):

        # super constructor
        super().__init__(type, depth)

        # tags
        self.tag_curve = "xf_keycurve"

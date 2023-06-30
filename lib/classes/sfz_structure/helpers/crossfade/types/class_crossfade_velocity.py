# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Crossfade : Velocity
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


class CrossfadeVelocity(Crossfade):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, type, depth):

        # super constructor
        super().__init__(type, depth)

        # tags
        self.tag_range = "vel"
        self.tag_curve = "xf_velcurve"

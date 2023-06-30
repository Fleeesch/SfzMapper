# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Crossfade
#
#   Abstract crossfade representation used for
#   printing data for either tonal or level crossfades
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Crossfade():

    tag_velocity = "xf_velcurve"
    tag_cc = "xf_cccurve"
    tag_tonal = "xf_keycurve"

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, type, depth):

        # store attributes
        self.type = type
        self.depth = depth

        # sfz tags
        self.tag_range = ""
        self.tag_curve = ""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        # return string
        data = ""

        # assume type is linear (gain)
        type_value = "gain"
        
        # use power type as an alternative
        if self.type.lower() == "power":
            type_value = "power"
        else:
            type_value = "gain"
        
        # curve sfz line (only of crossfade is > 0 )
        if self.depth != 0:
            data += self.tag_curve + "=" + type_value

        # return sfz string
        return data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Filter : Type
#
#   Represents a filter type
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FilterType():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, filter):

        # store relations
        self.filter = filter
        self.instrument = self.filter.instrument

        # poles
        self.poles = 1

        # available poles
        self.poles_lookup = None

        # tag for sfz
        self.tag = ""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Poles
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_poles(self, poles):

        if self.poles_lookup is None:
            return

        # go through available poles
        for i in self.poles_lookup:
            # pole count matches? set pole value
            if poles == i:
                self.poles = i
                return

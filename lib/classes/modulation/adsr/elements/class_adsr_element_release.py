# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : ADSR : Element : Release
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.adsr.elements.class_adsr_element_shapeable import AdsrElementShapeable

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class AdsrElementRelease(AdsrElementShapeable):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, adsr):

        self.tag = "_release"

        super().__init__(adsr, 0.01)

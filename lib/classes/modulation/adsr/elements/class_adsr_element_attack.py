# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : ADSR : Element : Attack
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.adsr.elements.class_adsr_element_shapeable import \
    AdsrElementShapeable

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class AdsrElementAttack(AdsrElementShapeable):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, adsr):

        self.tag = "_attack"

        super().__init__(adsr, 0.01)

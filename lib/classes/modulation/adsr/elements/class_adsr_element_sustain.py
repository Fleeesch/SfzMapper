# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : ADSR : Element : Sustain
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import math
from lib.classes.modulation.adsr.elements.class_adsr_element import AdsrElement

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class AdsrElementSustain(AdsrElement):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, adsr):

        self.tag = "_sustain"

        super().__init__(adsr, 1)

        # sustain factor
        self.value.factor = 100

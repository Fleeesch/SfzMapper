# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulatable : Modulation Type : Multiply
#
#   ARIA exclusive modulation type,
#   either addition or multiplication
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.interfaces.type.class_modulatable_modtype import ModulationType

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ModulationTypeMultiply(ModulationType):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self):

        # super constuctor
        super().__init__()

        # tag
        self.tag = "mult"

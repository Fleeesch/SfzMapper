# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Pedal : Sustain
#
#   Sustain Pedal configuration
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


from lib.classes.sfz_structure.control.pedal.class_pedal import Pedal

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class PedalSustain(Pedal):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, cc=64, off_value=0.5):
        
        # jump back to default value
        if not cc:
            cc = 66
        
        super().__init__(cc, off_value)
        
        self.tag = "sustain"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Pedal
#
#   Represents a Pedal configuration
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Pedal():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, cc=-1, off_value=1):
        
        # store vlaues
        self.cc = cc
        self.off_value = off_value
        
        
        self.tag = ""
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Sfz
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz(self):
        
        data = ""
        
        # don't return anything if there's no tag
        if not self.tag:
            return data

        # control change nr 
        data += self.tag + "_cc=" + str(self.cc) + "\n"
        
        # off value
        if self.off_value:
            data += self.tag + "_lo=" + str(self.off_value) + "\n"

        return data

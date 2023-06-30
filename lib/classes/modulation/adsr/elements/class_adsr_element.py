# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : ADSR : Element
#
#   Segment of an ADSR
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.adsr.elements.class_adsr_element_value import \
    AdsrElementValue
from lib.config import config
from lib.interfaces.modulatable import get_modulation_cc as get_cc

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class AdsrElement():
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, adsr, value):
        
        # source dasr
        self.adsr = adsr
        
        # value element
        self.value = AdsrElementValue(self, value)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Value
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def set_value(self, value):
        # set value element value
        self.value.set(value)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Value
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_value(self):
        # get value element value
        return self.value.get()
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def load_modulation(self, data):
        
        # ignore empty modulation section
        if data["modulation"] is None:
            return
        
        # try loading modulation
        try:
            # go through modulation elements
            for mod in data["modulation"]["cc"]:
                # merge modulation section with defaults
                data["modulation"]["cc"][mod] = config.merge_with_defaults(data["modulation"]["cc"][mod], "modulation adsr element")
                
                # default factor is 1:1
                factor = 1
                
                # correctional factor for sustain (goes from 0 to 100)
                if mod == "sustain":
                    factor = 100

                # store depth
                data["modulation"]["cc"][mod]["depth"] = data["modulation"]["cc"][mod]["depth"] * factor

            # add cc modulation to value element
            get_cc.get_modulation_cc(self.value, data["modulation"])
        except:
            pass

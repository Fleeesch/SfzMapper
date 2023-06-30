# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Filter : Resonance
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.modulators import class_modulation_cc as mod_cc
from lib.classes.modulation.modulators import class_modulation_var as mod_var
from lib.classes.modulation.modulators import class_modulation_envelope as mod_env
from lib.classes.modulation.modulators import class_modulation_lfo as mod_lfo
from lib.classes.sfz_structure.attributes.class_attribute import Attribute

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class FilterResonance(Attribute):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, filter, depth=0):

        # super constructor
        super().__init__(filter.instrument)
        
        # store sttribuates
        self.filter = filter
        self.depth = depth

        # sfz tag
        self.tag = "resonance"

        # modulation candidates
        self.set_modulation_candidates(mod_cc.ModulationCC, mod_var.ModulationVariable, mod_env.ModulationEnvelope, mod_lfo.ModulationLfo)

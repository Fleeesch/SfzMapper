# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : LFO : Rate
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_lfo_value import LfoValue

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class LfoRate(LfoValue):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, lfo):
        
        from lib.classes.modulation.modulators import \
            class_modulation_cc as ref_cc        
        
        from lib.classes.modulation.modulators import \
            class_modulation_lfo as ref_lfo
        
        from lib.classes.modulation.modulators import \
            class_modulation_envelope as ref_env
        
        # super constructor
        super().__init__(instrument, lfo)
        
        # sfz tag
        self.tag = self.lfo.tag + "_freq"
        
        # alternative modulation candidates
        self.set_modulation_candidates(ref_cc.ModulationCC, ref_lfo.ModulationLfo, ref_env.ModulationEnvelope)
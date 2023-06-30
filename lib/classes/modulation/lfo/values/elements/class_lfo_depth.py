# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : LFO : Depth
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_lfo_value import LfoValue

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class LfoDepth(LfoValue):
    
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
        self.tag = self.lfo.tag + "_depth"
        
        self.factor = 100
        
        # alternative modulation candidates
        self.set_modulation_candidates(ref_cc.ModulationCC, ref_lfo.ModulationLfo, ref_env.ModulationEnvelope)
        
        
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Modulation SFZ Tag
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    #def get_modulation_data(self):
    #    
    #    # return data
    #    mod_data = {}
    #    
    #    # go through modulators
    #    for mod in self.modulations:
    #        
    #        # get CC Index of possible CC modulation, skip if there isn't any    
    #        try:
    #            cc = mod.cc
    #        except:
    #            continue
    #        
    #        # get modulation attributes
    #        depth = mod.depth
    #        smooth = mod.smooth
    #        step = mod.step
    #        
    #        # declare cc as dict
    #        mod_data[cc] = {}
    #        
    #        # store data in cc dict adress
    #        mod_data[cc]["depth"] = depth
    #        mod_data[cc]["smooth"] = smooth
    #        mod_data[cc]["step"] = step
    #    
    #    # return collected data>>>
    #    return mod_data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulation : LFO
#
#   Modulation emerging from a LFO
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_modulation import Modulation
from lib.interfaces.int_modulatable import Modulatable
from lib.config.reformat.reformat_modulation_attribute import reformat_modulation_attribute as reformat_attribute

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ModulationLfo(Modulation, Modulatable):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, modulatable, mod_data, lfo, depth):
        
        import lib.classes.modulation.modulators.class_modulation_cc as ref_cc
        import lib.classes.modulation.modulators.class_modulation_envelope as ref_env
        
        # super constructor
        Modulatable.__init__(self,modulatable.instrument)
        Modulation.__init__(self,modulatable, depth)
        
        # store envelope
        self.lfo = lfo
        
        # set modulation candidates
        self.set_modulation_candidates(ref_cc.ModulationCC, ref_env.ModulationEnvelope)
        
        # reformat modulation data
        reformat_attribute(mod_data["modulation"])        
        
        # load modulation data
        self.add_modulation(mod_data["modulation"])        
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Depth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_depth(self, source=None):

        import lib.classes.modulation.lfo.values.class_lfo_value as ref_lfo

        data = ""
        
        # -----------------------------------
        # LFO Exception
        # -----------------------------------

        # lfo gets different formatting
        if isinstance(source, ref_lfo.LfoValue):

            # split modulator tag for tag reversal
            tags = self.modulator.tag.split("_")

            # skip if tag isn't valid in the first place
            if len(tags) < 2:
                return ""

            # build return string
            data += self.lfo.tag + "_" + tags[1] + "_" + tags[0] + "=" + str(self.depth * self.modulator.factor) + "\n"
            data += "\n"

            # return data
            return data

        # -----------------------------------
        # Normal Modulation
        # -----------------------------------
        
        # constant depth
        if self.depth:
            data += self.lfo.tag + "_" + self.modulator.tag + "=" + str(self.depth * self.modulator.factor) + "\n"
        
        # -----------------------------------
        # CC Modulation
        # -----------------------------------
        
        for mod in self.modulations:
            data += mod.get_sfz_depth(self) + "\n"
            data += mod.get_sfz_curve(self) + "\n"
            data += mod.get_sfz_smooth(self) + "\n"
            data += mod.get_sfz_step(self) + "\n"
    
        return data
        
        
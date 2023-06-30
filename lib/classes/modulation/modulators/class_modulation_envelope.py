# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulation : Envelope
#
#   Modulation emerging from an envelope
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


class ModulationEnvelope(Modulation, Modulatable):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, modulatable, mod_data, envelope, depth):
        
        from lib.classes.modulation.modulators import class_modulation_cc as ref_cc
        
        # super constructor
        Modulatable.__init__(self,modulatable.instrument)
        Modulation.__init__(self,modulatable, depth)
        
        # store envelope
        self.envelope = envelope
        
        # set modulation candidates
        self.set_modulation_candidates(ref_cc.ModulationCC)
        
        
        # reformat modulation data
        reformat_attribute(mod_data["modulation"])
        
        # load modulation data
        self.add_modulation(mod_data["modulation"])
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Depth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_depth(self, source=None):
        
        import lib.classes.modulation.modulators.class_modulation_lfo as ref_lfo
        import lib.classes.modulation.lfo.values.class_lfo_value as ref_lfo_val
        
        # return string
        data = ""
        
        # -----------------------------------
        # LFO Exception
        # -----------------------------------
        
        # lfo gets different formatting
        if 1==2 and isinstance(source, ref_lfo.ModulationLfo):
            
            # split modulator tag for tag reversal
            tags = source.lfo.tag.split("_")
            
            # skip if tag isn't valid in the first place
            if len(tags) < 2:
                return ""
            
            # build return string
            data += "eg" + str(self.envelope.index) + "_" + tags[1] + "_" + tags[0] + "=" + str(self.depth * self.modulator.factor) + "\n"
            
            # return data
            return data
        
        # -----------------------------------
        # LFO Value Exception
        # -----------------------------------
        
        # lfo gets different formatting
        if isinstance(source, ref_lfo_val.LfoValue):
            
            # split modulator tag for tag reversal
            tags = self.modulator.tag.split("_")
            
            # skip if tag isn't valid in the first place
            if len(tags) < 2:
                return ""

            # build return string
            data += "eg" + str(self.envelope.index) + "_" + tags[1] + "_" + tags[0] + "=" + str(self.depth * self.modulator.factor) + "\n"
            
            # return data
            return data
        
        
        # -----------------------------------
        # Normal Modulation
        # -----------------------------------
        
        data += "eg" + str(self.envelope.index) + "_" + self.modulator.tag + "=" + str(self.depth * self.modulator.factor) + "\n"
    
        # -----------------------------------
        # CC Modulation
        # -----------------------------------
        
        for mod in self.modulations:
            data += mod.get_sfz_depth(self) + "\n"
            data += mod.get_sfz_curve(self) + "\n"
            data += mod.get_sfz_smooth(self) + "\n"
            data += mod.get_sfz_step(self) + "\n"
    
        return data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Interface : Modulatable
#
#   Can be used via Inheritance to make any class
#   modulatable via Modulator Classes.
#
#   Limited to a singular 'depth' value that can
#   be modulated.
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from .modulatable import get_modulation_cc as mod_cc
from .modulatable import get_modulation_envelope as mod_env
from .modulatable import get_modulation_lfo as mod_lfo
from .modulatable import get_modulation_variable as mod_var
from .modulatable import get_modulation_velocity as mod_vel

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Modulatable:
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, instrument):
        
        from lib.interfaces.compensation.class_modulatable_compensation_sum import \
            ModulatableCompensationSum
        
        # instrument
        self.instrument = instrument
        
        # empty candidate list by default
        self.modulation_candidates = []
        
        # modulations and envelopes
        self.modulations = []
        
        # depth (singular level)
        self.depth = None
        
        # linked curve
        self.curve = None
        
        # modulation factor
        self.factor = 1
        
        # use audio engine modulation type by default
        self.mod_type = None
        
        # use sum compensation by default
        self.compensation = ModulatableCompensationSum(self)
        
        self.skip_depth = False
        self.skip_smooth = False
        self.skip_step = False
        self.skip_curve = False
        
        # sfz tag
        self.tag = ""
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Compensation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def set_compensation(self, compensation):
        self.compensation = compensation
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Modulation Type
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_modulation_type(self, mod_type):

        # sets the modulation type
        self.mod_type = mod_type

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Modulation Candidates
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_modulation_candidates(self, *tags):

        # just store tags to prevent circular import
        self.modulation_candidates = tags

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Is Modulation Candidate
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def is_modulation_candidate(self, mod):
        
        # go through candidates
        for m in self.modulation_candidates:

            # candidate matches? return true
            if m == mod:
                return True

        # no candidate found
        return False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Modulation (All)
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def add_modulation(self, data):
        
        from lib import lookup
        
        # try loading modulation type, keep empty on fail
        try:
            mod_type = data["type"]
            if mod_type:
                self.set_modulation_type(lookup.MODTYPE_LOOKUP[mod_type]())
        except:
            pass
        
        # try loading compensation type, keep empty on fail
            try:
                comp_type = data["compensation"]
                
                if comp_type:
                    self.set_compensation(lookup.COMPENSATION_TYPE[comp_type]())
            except:
                pass
        
        # skip if data is empty
        if not data:
            return        
        
        # get velocity modulation
        mod_vel.get_modulation_velocity(self, data)
        
        # get CCs modulation
        mod_cc.get_modulation_cc(self, data)
        
        # get envelope modulation
        mod_env.get_modulation_envelope(self, data)
        
        # get LFOs modulation
        mod_lfo.get_modulation_lfo(self, data)
        
        # get variables modulation
        mod_var.get_modulation_variable(self, data)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Get Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_modulation(self):
        
        lines = []
        
        # add type tag if modulation and a defined mot type exists
        if self.modulations and self.mod_type:
            lines.append(self.tag + "_mod=" + self.mod_type.get_sfz_tag())

        # go through modulations
        for mod in self.modulations:
            
            # get detph
            if not self.skip_depth:
                if mod.depth or mod.depth_ignore_defaults:

                    # load line
                    line = mod.get_sfz_depth(self)
                    
                    # only append if not empty
                    if line:
                        lines.append(line)

            # get smoothing
            if not self.skip_smooth:
                if mod.smooth or mod.smooth_ignore_defaults:

                    # load line
                    line = mod.get_sfz_smooth(self)

                    # only append if not empty
                    if line:
                        lines.append(line)
            
            # get stepping
            if not self.skip_step:
                if mod.step or mod.step_ignore_defaults:

                    # load line
                    line = mod.get_sfz_step(self)

                    # only append if not empty
                    if line:
                        lines.append(line)
            
            # get curve
            if not self.skip_curve:
                if mod.curve:

                    # index valid? Add curve reference tag
                    if mod.curve.index:

                        # load line
                        line = mod.get_sfz_curve(self)
                        
                        # only append if not empty
                        if line:
                            lines.append(line)
        
        # return constructed line array
        return lines

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Calculate Compensation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def calculate_compensation(self):
        
        # return compensation value unless there isn't any available
        if self.compensation:
            return self.compensation.get_value() * self.factor
        else:
            return 0

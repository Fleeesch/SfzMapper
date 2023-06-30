# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulatable : Attribute
#
#   A single Attribute representing a SFZ tag
#   that can be modulated using various modulators
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


from lib.interfaces.int_modulatable import Modulatable

from ...modulation.modulators import class_modulation_cc as mod_cc
from ...modulation.modulators import class_modulation_envelope as mod_env
from ...modulation.modulators import class_modulation_lfo as mod_lfo
from ...modulation.modulators import class_modulation_var as mod_var
from ...modulation.modulators import class_modulation_velocity as mod_vel

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Attribute(Modulatable):
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Add from Tag
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def add_from_tag(instrument, data, tag):
        
        from lib import lookup
        
        # try returning class from lookup table
        try:
            return lookup.ATTRIBUTE_LOOKUP[tag](instrument, data["level"])
        except:
            return None
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, instrument):
        
        # super constructor
        super().__init__(instrument)
        
        # instrument reference
        self.instrument = instrument
        
        # attribute level
        self.level = 0
        
        # modulation candidates
        self.set_modulation_candidates(
            mod_vel.ModulationVelocity,
            mod_cc.ModulationCC,
            mod_env.ModulationEnvelope,
            mod_var.ModulationVariable,
            mod_lfo.ModulationLfo
        )

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Get Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_lines(self):

        lines = []

        # get line arrays from individual settings
        lines_setting = self.get_setting()
        lines_modulation = self.get_modulation()

        # append lines to return array
        for line in lines_setting:
            lines.append(line)

        for line in lines_modulation:
            lines.append(line)
        
        # return array of lines
        return lines

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Get Setting
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_setting(self):

        lines = []
        
        # get compensation value
        compensation = self.calculate_compensation()

        # append attribute level
        if self.level is not None:
            
            lines.append(self.tag + "=" + str((self.level + compensation) * self.factor))
            pass
        
        return lines

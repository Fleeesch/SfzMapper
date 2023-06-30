# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Variable
#
#   Class representing a SFZ Variable, supported by
#   exclusively by ARIA
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.interfaces.int_modulatable import Modulatable

from .modulation.modulators import class_modulation_cc as mod_cc

from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Variable(Modulatable):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, name):

        # super constructor
        super().__init__(instrument)
        
        # store name
        self.name = name
        
        # store variable in instrument lookup list
        self.instrument.variables[name] = self
        
        from lib.config.reformat import \
            reformat_modulation_attribute as reformat
        
        # get data
        self.data = self.instrument.map_data["variables"][name]
        
        # merge data with defaults
        self.data = config.merge_with_defaults(self.data, "variable element")
        
        # reformat modulation
        self.data["modulation"] = reformat.reformat_modulation_attribute(self.data["modulation"])
        
        # store index
        self.index = instrument.variable_index
        
        # construct tag
        self.tag = "var" + str(self.index)
        
        # variable specific tag
        self.variable_tag = "var" + str(self.index)
        
        # increment index
        instrument.variable_index += 1
        
        # modulations
        self.modulations = []

        # setup modulators
        self.set_modulation_candidates(mod_cc.ModulationCC)

        # add modulation
        self.add_modulation(self.data["modulation"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get(self):
        # return data
        data = ""

        # go through modulations
        for mod in self.modulations:
            # collect depth and curve lines
            data += mod.get_sfz_depth(self) + "\n"
            data += mod.get_sfz_curve(self) + "\n"

        # return sfz line block
        return data

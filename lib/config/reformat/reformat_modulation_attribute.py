# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Modulation : Attributes
#
#   Formatting functionality for the
#   modulation section of attributes
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


from . import reformat_modulation as ref_mod
from .attribute import reformat_modulation_attribute_cc as ref_cc
from .attribute import reformat_modulation_attribute_lfo as ref_lfo
from .attribute import reformat_modulation_attribute_envelope as ref_env
from .attribute import reformat_modulation_attribute_variable as ref_var
from .attribute import reformat_modulation_attribute_velocity as ref_vel

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Modulation Section
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_modulation_attribute(data):
    
    # aria velocity remap
    data = ref_mod.implement_aria_remap(data)
    
    # velocity
    data = ref_vel.reformat_modulation_velocity(data)
    
    # cc
    data = ref_cc.reformat_modulation_cc(data)
    
    # lfo
    data = ref_lfo.reformat_modulation_lfo(data)

    # envelope
    data = ref_env.reformat_modulation_envelope(data)

    # variable
    data = ref_var.reformat_modulation_variable(data)

    return data

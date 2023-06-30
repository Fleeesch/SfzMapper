# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Modulation : LFO
#
#   Modulation of LFO Attributes
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.config import config

from . import reformat_modulation as ref_mod

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Modulation Section
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_modulation_lfo(data):
    
    data = ref_mod.implement_aria_remap(data)
    
    # go through modulation candidates
    for mod_type in ["cc","lfo","envelopes"]:
        
        # elements that can be removed
        remove_element = []
        
        # skip if there's no data or the data is invalid
        try:
            if data[mod_type] is None:
                continue
        except:
            continue

        # go through mod elements of section (cast as list since default merge might add data)
        for mod_element in list(data[mod_type]):

            # merge section with defaults
            data[mod_type][mod_element] = config.merge_with_defaults(data[mod_type][mod_element], "modulation element")
        
        # remove listed elements from type
        for mod_element in remove_element:
            data[mod_type].pop(mod_element)

    return data

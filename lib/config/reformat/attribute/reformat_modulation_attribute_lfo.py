# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Modulation : CC
#
#   Reformats the CC section of a
#   Modulation settings segment
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Modulation CC
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_modulation_lfo(data):

    # list of LFOs to be removed
    remove_lfo = []

    try:
        
        for mod in data["lfo"]:
            
            # merge lfo mod section with defaults
            data["lfo"][mod] = config.merge_with_defaults(data["lfo"][mod], "modulation lfo element")
            
            # mark LFOS for removal that have a modulation depth of 0,
            # but keep it if modulation is available
            if data["lfo"][mod]["depth"] == 0 and not data["lfo"][mod]["modulation"]:
                remove_lfo.append(mod)
    
    except:
        pass
    
    # remove marked CCs
    for mod in remove_lfo:
        data["lfo"].pop(mod)
    
    return data

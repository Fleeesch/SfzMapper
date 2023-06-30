# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Modulation : Velocity
#
#   Reformats the Velocity section of a
#   Modulation settings segment
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Modulation Velocity
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_modulation_velocity(data):

    # single instance elements
    mod_elements = ["velocity"]

    # list of instances to be removed
    mod_remove = []

    try:
        for mod in mod_elements:

            # merge modulation section with defaults
            data[mod] = config.merge_with_defaults(data[mod], "modulation element")

            # mark section where depth is 0 for removal
            if data[mod]["depth"] == 0:
                mod_remove.append(mod)

    except:
        pass

    # remove markted instances
    for mod in mod_remove:
        data.pop(mod)

    return data

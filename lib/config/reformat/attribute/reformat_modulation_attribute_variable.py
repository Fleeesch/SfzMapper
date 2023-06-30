# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Modulation : Variable
#
#   Reformats the Variable section of a
#   Modulation settings segment
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Modulation Variable
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_modulation_variable(data):

    # list of variables to be removed
    remove_var = []

    try:

        for mod in data["variables"]:

            # merge variable mod section with defaults
            data["variables"][mod] = config.merge_with_defaults(data["variables"][mod], "modulation element")

            # mark variables for removal that have a modulation depth of 0
            if data["variables"][mod]["depth"] == 0:
                remove_var.append(mod)
    
    except:
        pass
    
    # remove marked variables
    for mod in remove_var:
        data["variables"].pop(mod)

    return data

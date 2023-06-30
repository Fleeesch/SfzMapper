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


def reformat_modulation_cc(data):

    # list of CCs to be removed
    remove_cc = []

    try:

        for mod in data["cc"]:

            # merge cc mod section with defaults
            data["cc"][mod] = config.merge_with_defaults(data["cc"][mod], "modulation element")

            # mark CCS for removal that have a modulation depth of 0
            if data["cc"][mod]["depth"] == 0:
                remove_cc.append(mod)

    except:
        pass

    # remove marked CCs
    for mod in remove_cc:
        data["cc"].pop(mod)

    return data

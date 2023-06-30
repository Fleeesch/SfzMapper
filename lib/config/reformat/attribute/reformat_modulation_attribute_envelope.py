# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Modulation : Envelope
#
#   Reformats the Envelope section of a
#   Modulation settings segment
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Modulation Envelope
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_modulation_envelope(data):

    # list of envelopes to be removed
    remove_env = []
    
    try:

        for mod in data["envelopes"]:

            # merge envelope mod section with defaults
            data["envelopes"][mod] = config.merge_with_defaults(data["envelopes"][mod], "envelope element")

            # mark envelopes for removal that have a modulation depth of 0,
            # but keep the ones that have internal modulation data
            if data["envelopes"][mod]["depth"] == 0 and not data["envelopes"][mod]["modulation"]:
                remove_env.append(mod)
    
    except:
        pass

    # remove marked envelopes
    for mod in remove_env:
        data["envelopes"].pop(mod)

    return data

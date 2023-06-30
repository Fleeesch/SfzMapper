# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Functions
#
#   Calculations and useful functions to
#   do simple deeds
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import re

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Filter Number
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def filter_number(input):
    
    # try filtering a number through int casting
    try:
        return int(re.sub('\D', '', input))
    except:    
        # return 0 on fail
        return 0
    
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Filter String
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def filter_string(input):
    return re.sub(r'[0-9]', '', input)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Limit
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def limit(val, val_min, val_max):
    # limit range of value
    return min(max(val, val_min), val_max)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Rescale Value
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def rescale_value(val, in_l, in_h, out_l, out_h):

    # don't rescale no range is given
    if in_l == in_h or out_l == out_h:
        return out_l

    # rescale algorithm
    rtn = (val - in_l) * (out_h - out_l) / (in_h - in_l) + out_l

    # keep values within output range
    if rtn < out_l:
        return out_l

    return min(rtn, out_h)

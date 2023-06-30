# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : Amp EG
#
#   Amplitude Envelope
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat Amp EG
# - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_ampeg(data):
    
    # go through attributes
    for part in ["delay", "attack", "decay", "sustain", "hold", "release"]:
        
        # try rearranging data
        try:
            # data is a single number?
            if type(data[part]) is float or type(data[part]) is int:
                
                # store value
                val = data[part]
                
                # transform into dict
                data[part] = {}
                
                # copy value into level attribute
                data[part]["level"] = val
            
        except:
            continue
    
    # return modified data
    return data
            
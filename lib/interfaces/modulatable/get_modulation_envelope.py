# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Get Modulation : Envelope
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_modulation_envelope(source, data):

    import lib.classes.modulation.modulators.class_modulation_envelope as mod_env
    from lib import lookup
    from lib.config import config
    
    # skip if modulation type isn't valid
    if not source.is_modulation_candidate(mod_env.ModulationEnvelope):
        return
    
    # don't process empty or missing list
    try:
        if data["envelopes"] is None:
            return
    except:
        return
    
    # go through envelopes
    for env in data["envelopes"]:
        
        # try implementing envelope modulation
        try:
            
            # try to load depth (might raise exception)
            mod_depth = data["envelopes"][env]["depth"]
            
            # create or just get envelope
            envelope = lookup.add_envelope_via_lookup(source.instrument, env)
            
            # merge internal modulation daa with default values
            data["envelopes"][env] = config.merge_with_defaults(data["envelopes"][env], "modulation element")
            
            # create modulation instance, append to lookup
            mod = mod_env.ModulationEnvelope(source, data["envelopes"][env] ,envelope, mod_depth)
            
            # append modulation to lookup
            source.modulations.append(mod)

        except:
            pass

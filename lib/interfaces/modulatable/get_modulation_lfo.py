# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Get Modulation : LFO
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_modulation_lfo(source, data):
    
    import lib.classes.modulation.modulators.class_modulation_lfo as mod_lfo
    from lib import lookup
    from lib.config import config
    
    # skip if modulation type isn't valid
    if not source.is_modulation_candidate(mod_lfo.ModulationLfo):
        return
    
    # don't process empty or missing list
    try:
        if data["lfo"] is None:
            return
    except:
        return
    
    # go through all the LFOs
    for lfo in data["lfo"]:
        
        # try implementing the lfo
        try:
            
            # create lfo via lookup
            lfo_new = lookup.add_lfo_via_lookup(source.instrument, lfo)
            
            # load modulation attributes
            mod_depth = data["lfo"][lfo]["depth"]
            
            # ::: CC Modulation :::
            
            # get modulation depth
            mod_depth = data["lfo"][lfo]["depth"]
            
            # store attributes for direct lfo modulation
            mod_comp = data["lfo"][lfo]["compensate"]
            
            # merge internal modulation daa with default values
            data["lfo"][lfo] = config.merge_with_defaults(data["lfo"][lfo], "modulation element")
            
            # create modulation
            mod = mod_lfo.ModulationLfo(source, data["lfo"][lfo], lfo_new, mod_depth)
            mod.compensation = mod_comp
            
            # append modulation to lookup
            source.modulations.append(mod)
        
        except:
            pass

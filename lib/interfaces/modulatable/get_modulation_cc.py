# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Get Modulation : CC
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_modulation_cc(source, data):
    
    import lib.classes.modulation.modulators.class_modulation_cc as mod_cc
    from lib import lookup
    
    # skip if modulation type isn't valid
    if not source.is_modulation_candidate(mod_cc.ModulationCC):
        return
    
    # don't process empty or missing list
    try:
        if data["cc"] is None:
            return
    except:
        return

    # go through all possible cc numbers
    for cc in data["cc"]:
        
        # try implementing cc modulation
        try:
            
            # try to get control instance
            ctrl_inst = source.instrument.controls[cc]

            # try to load depth (might raise exception)
            mod_depth = data["cc"][cc]["depth"]
            mod_curve = data["cc"][cc]["curve"]
            mod_comp = data["cc"][cc]["compensate"]
            mod_smooth = data["cc"][cc]["smooth"]
            mod_step = data["cc"][cc]["step"]
            
            # add or get curve via lookup
            crv = lookup.add_curve_via_lookup(source.instrument, mod_curve)
            
            # create modulation instance, append to lookup
            mod = mod_cc.ModulationCC(source, ctrl_inst.cc, mod_depth)
            mod.set_curve(crv)
            mod.set_compensation(mod_comp)
            mod.set_smooth(mod_smooth)
            mod.set_step(mod_step)
            
            # append modulation to lookup
            source.modulations.append(mod)
        
        except:
            pass

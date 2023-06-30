# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Get Modulation : Variable
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_modulation_variable(source, data):
    
    import lib.classes.modulation.modulators.class_modulation_var as mod_var
    from lib import lookup

    # skip if modulation type isn't valid
    if not source.is_modulation_candidate(mod_var.ModulationVariable):
        return

    # don't process empty list
    if data["variables"] is None:
        return

    # go through variables
    for var in data["variables"]:

        # try implementing variable modulation
        try:

            # try to load depth (might raise exception)
            mod_depth = data["variables"][var]["depth"]
            mod_comp = data["variables"][var]["compensate"]
            
            variable = lookup.add_variable_via_lookup(source.instrument, var)
            
            # create modulation instance, append to lookup
            mod = mod_var.ModulationVariable(source, variable.index, mod_depth)
            
            mod.set_compensation(mod_comp)
            
            # append modulation to lookup
            source.modulations.append(mod)
        
        except:
            pass

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Get Modulation : Velocity
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_modulation_velocity(source, data):

    import lib.classes.modulation.modulators.class_modulation_velocity as mod_vel
    from lib import lookup

    # skip if modulation type isn't valid
    if not source.is_modulation_candidate(mod_vel.ModulationVelocity):
        return
    
    # try implementing velocity modulation
    try:
        
        # try to load depth (might raise exception)
        mod_depth = data["velocity"]["depth"]
        mod_curve = data["velocity"]["curve"]
        mod_comp = data["velocity"]["compensate"]

        crv = lookup.add_curve_via_lookup(source.instrument, mod_curve)

        # create modulation instance, append to lookup
        mod = mod_vel.ModulationVelocity(source, mod_depth)
        mod.set_compensation(mod_comp)

        # append modulation to lookup
        source.modulations.append(mod)

    except:
        pass

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Get Modulation : Envelope : Points
#
#   Retrieves modulation for envelope points of a
#   given envelope
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Dependencies
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

import lib.classes.modulation.modulators.class_modulation_cc as mod_ref_cc

from lib import lookup

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add Modulation : Envelope : Points
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def get_modulation_envelope_points(source, data):
    
    # go through modulation types
    for mod_type in ["cc"]:
        
        # skip if there's no data
        if data[mod_type] is None:
            continue
        
        # go through modulation elements
        for mod_element in data[mod_type]:
            
            # store data address
            mod = data[mod_type][mod_element]
            
            try:
                
                # get control type of modulation element
                ctrl = source.instrument.controls[mod_element]
                
                # go through list of modulations
                for idx, m in enumerate(mod["points"]):
                 
                    # time modulation (optionally with curve)
                    if len(m) < 4:
                        add_point_mod(source.points[idx].time, ctrl.cc, m[0])
                        add_point_mod(source.points[idx].level, ctrl.cc, m[1])
                    else:
                        add_point_mod(source.points[idx].time, ctrl.cc, m[0], m[1])
                        add_point_mod(source.points[idx].level, ctrl.cc, m[2], m[3])
                    
            except:
                pass


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add Point Mod
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def add_point_mod(source, mod_element, depth, curve=None):
    
    # declare mod
    mod = None
    
    # add mod of modulation is available
    if depth != 0:
        mod = mod_ref_cc.ModulationCC(source, mod_element, depth)
    
    # append mod to lookup if created
    if mod:
        source.modulations.append(mod)
        
        # add curve if there's a viable reference
        if curve:
            crv_new = lookup.add_curve_via_lookup(source.instrument, curve)
            mod.curve = crv_new    

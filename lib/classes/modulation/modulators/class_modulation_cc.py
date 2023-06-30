# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulation : CC
#
#   Modulation emerging from a CC
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_modulation import Modulation

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ModulationCC(Modulation):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, modulatable, cc, depth):

        # super constructor
        super().__init__(modulatable, depth)

        # store settings
        self.cc = cc

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Depth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz_depth(self, source=None):

        import lib.classes.class_variable as ref_var
        import lib.classes.modulation.modulators.class_modulation_envelope as ref_mod_env
        import lib.classes.modulation.modulators.class_modulation_lfo as ref_mod_lfo
        
        # Modulation LFO
        if isinstance(source, ref_mod_lfo.ModulationLfo):
            return source.lfo.tag + "_" + source.modulator.tag + "_oncc" + str(self.cc) + "=" + str(self.depth * self.modulator.factor)
        
        # Modulation Envelope
        if isinstance(source, ref_mod_env.ModulationEnvelope):
            return source.envelope.tag + "_" + source.modulator.tag + "_oncc" + str(self.cc) + "=" + str(self.depth * self.modulator.factor)
        
        # Variable Exception
        if isinstance(source, ref_var.Variable):
            return source.variable_tag + "_oncc" + str(self.cc) + "=" + str(self.depth * self.modulator.factor)
        
        # Attribute
        return self.modulator.tag + "_oncc" + str(self.cc) + "=" + str(self.depth * self.modulator.factor)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Smooth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz_smooth(self, source=None):
        
        import lib.classes.class_variable as ref_var
        import lib.classes.modulation.envelope.point_values.class_envelope_point_value as ref_env
        import lib.classes.modulation.modulators.class_modulation_envelope as ref_mod_env
        import lib.classes.modulation.modulators.class_modulation_lfo as ref_mod_lfo
        
        # Modulation LFO
        if isinstance(source, ref_mod_lfo.ModulationLfo):
            return source.lfo.tag + "_" + source.modulator.tag + "_smoothcc" + str(self.cc) + "=" + str(self.smooth)
        
        # Modulation Envelope
        if isinstance(source, ref_mod_env.ModulationEnvelope):
            return source.envelope.tag + "_" + source.modulator.tag + "_smoothcc" + str(self.cc) + "=" + str(self.smooth)
        
        # Variable Exception
        if isinstance(source, ref_var.Variable):
            return source.variable_tag + "_smoothcc" + str(self.cc) + "=" + str(self.smooth)
        
        # Envelope exception
        if isinstance(source, ref_env.EnvelopePointValue):
            return ""
        
        # Attribute
        return self.modulator.tag + "_smoothcc" + str(self.cc) + "=" + str(self.smooth)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Curve
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz_curve(self, source=None):
        
        import lib.classes.class_variable as ref_var
        import lib.classes.modulation.modulators.class_modulation_envelope as ref_mod_env
        import lib.classes.modulation.modulators.class_modulation_lfo as ref_mod_lfo
        
        # only return something if there's a curve
        if self.curve is None:
            return ""
        
        # Modulation LFO
        if isinstance(source, ref_mod_lfo.ModulationLfo):
            return source.lfo.tag + "_" + source.modulator.tag + "_curvecc" + str(self.cc) + "=" + str(self.curve.index)
        
        # Modulation Envelope
        if isinstance(source, ref_mod_env.ModulationEnvelope):
            return source.envelope.tag + "_" + source.modulator.tag + "_curvecc" + str(self.cc) + "=" + str(self.curve.index)
        
        # Variable Exception
        if isinstance(source, ref_var.Variable):
            return source.variable_tag + "_curvecc" + str(self.cc) + "=" + str(self.curve.index)
        
        # Attribute
        return self.modulator.tag + "_curvecc" + str(self.cc) + "=" + str(self.curve.index)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Step
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz_step(self, source=None):
        
        import lib.classes.class_variable as ref_var
        import lib.classes.modulation.envelope.point_values.class_envelope_point_value as ref_env
        import lib.classes.modulation.modulators.class_modulation_envelope as ref_mod_env
        import lib.classes.modulation.modulators.class_modulation_lfo as ref_mod_lfo
        
        # Modulation LFO
        if isinstance(source, ref_mod_lfo.ModulationLfo):
            return source.lfo.tag + "_" + source.modulator.tag + "_stepcc" + str(self.cc) + "=" + str(self.step)
        
        # Modulation Envelope
        if isinstance(source, ref_mod_env.ModulationEnvelope):
            return source.envelope.tag + "_" + source.modulator.tag + "_stepcc" + str(self.cc) + "=" + str(self.step)
        
        # Variable Exception
        if isinstance(source, ref_var.Variable):
            return source.variable_tag + "_stepcc" + str(self.cc) + "=" + str(self.step)
        
        # Envelope exception
        if isinstance(source, ref_env.EnvelopePointValue):
            return ""
        
        # Attribute
        return self.modulator.tag + "_stepcc" + str(self.cc) + "=" + str(self.step)

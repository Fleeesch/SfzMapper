# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Modulation
#
#   Represents the link between a Modulator and
#   a Modulatable
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Modulation:
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, modulator, depth):
        
        # modulator reference
        self.modulator = modulator
        
        # default settings for modulator
        self.depth = depth
        self.curve = None
        self.compensation = False
        self.smooth = 0
        self.step = 0
        
        # ignore default values, always print sfz
        self.depth_ignore_defaults = True
        self.smooth_ignore_defaults = False
        self.step_ignore_defaults = False
        
        # sfz tag
        self.tag = ""
        self.tag_depth = ""
        self.tag_curve = ""
        self.tag_smooth = ""
        self.tag_step = ""

        # modulation formatter
        self.formatter = None

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Setter
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Depth

    def set_depth(self, depth):
        self.depth = depth

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Curve

    def set_curve(self, curve):
        self.curve = curve

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Compensation

    def set_compensation(self, compensation):
        self.compensation = compensation

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Smooth

    def set_smooth(self, smooth):
        self.smooth = smooth

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Smooth

    def set_step(self, step):
        self.step = step

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Getter
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Depth

    def get_amount(self):
        return self.depth

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Curve

    def get_curve(self, curve):
        return self.curve

    # * * * * * * * * * * * * * * * * * * * * * *
    #   Compensation

    def get_compensation(self, compensation):
        return self.compensation

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Depth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_depth(self, source=None):
        return ""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Curve
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_curve(self, source=None):
        return ""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Smooth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_smooth(self, source=None):
        return ""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Step
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_step(self, source=None):
        return ""

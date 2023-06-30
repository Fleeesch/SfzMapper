# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Envelope : Point
#
#   A point of a custom Envelope
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.envelope.point_values.class_envelope_point_level import \
    EnvelopePointLevel
from lib.classes.modulation.envelope.point_values.class_envelope_point_time import \
    EnvelopePointTime

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class EnvelopePoint():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, envelope, index, time, level, curvature, curve):
        
        # store attributes
        self.envelope = envelope
        self.index = index
        
        # characteristicsl
        self.time = EnvelopePointTime(self, time)
        self.level = EnvelopePointLevel(self, level)
        self.curvature = curvature
        self.curve = curve
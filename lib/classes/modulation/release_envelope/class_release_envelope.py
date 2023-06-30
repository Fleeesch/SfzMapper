# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Release Envelope
#
#   Release Envelope,
#   currently not supported by ARIA
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.release_envelope.class_release_envelope_point import \
    ReleaseEnvelopePoint

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ReleaseEnvelope():
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, source):
        
        # store attributes
        self.source = source
        self.instrument = source.instrument
        
        # standard decay
        self.decay = 0
        
        # points
        self.points = []
        
        # point index
        self.point_index = 1

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Add Point
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_point(self, time, depth):

        # add point
        self.points.append(ReleaseEnvelopePoint(self, time, depth))

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz(self):
        
        # data array
        data = ""
        
        # always add rt data flag
        data += "rt_dead=on" + "\n"
        
        if self.decay:
            data += "rt_decay=" + str(self.decay) + "\n"
        
        # go through points
        for point in self.points:
            # add point sfz to return array
            data += point.get_sfz()
        
        # return sfz data
        return data

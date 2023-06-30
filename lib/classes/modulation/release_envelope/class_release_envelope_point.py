# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Release Envelope : Point
#
#   Point of a Release Envelope
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ReleaseEnvelopePoint():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, envelope, time, depth):

        # store attributes
        self.envelope = envelope

        # store time
        self.time = time

        # store depth
        self.depth = depth

        # store point index
        self.index = envelope.point_index

        # increment envelope point index
        envelope.point_index += 1

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        # return string
        data = ""

        # add depth
        data += "rt_decay" + str(self.index) + "=" + str(self.depth) + "\n"

        # add time
        data += "rt_decay" + str(self.index) + "_time=" + str(self.time) + "\n"

        # return sfz string
        return data

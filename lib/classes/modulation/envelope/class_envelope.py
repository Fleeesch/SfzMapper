# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Envelope
#
#   Represents a custom Envelope supported
#   by the SFZ2 Standard
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.envelope.class_envelope_point import EnvelopePoint
from lib.config import config
import lib.lookup as lookup

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Envelope():
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, name, sustain, points):

        from lib.config.reformat import \
            reformat_modulation_envelope as reformat

        # store attributes
        self.instrument = instrument
        self.name = name
        self.index = None

        # adapt and increment index
        self.index = instrument.envelope_index
        instrument.envelope_index += 1

        # tag for sfz
        self.tag = "eg" + str(self.index)

        # dynamic recalculation
        self.dynamic = False

        # copy modulation data section and reformat it
        self.data = self.instrument.map_data["envelopes"][name]

        # merge data with defaults
        self.data = config.merge_with_defaults(self.data, "envelopes")

        # reformat modulation section
        self.data["modulation"] = reformat.reformat_modulation_envelope(self.data["modulation"])

        # points lookup
        self.points = []

        # automatic sustain point is disabled by default
        self.sustain_auto = False

        # relative sustain point offset
        self.sustain_relative = False

        # empty sustain by default
        self.sustain = None

        # activate auto sustain if there's no sustain point
        if sustain is None or sustain < 0:
            self.sustain_auto = True
        else:

            # activate optional relative sustain point
            if sustain < 0:
                self.sustain_relative = True

            # fixed sustain point
            self.sustain = sustain

        # add points via passed list
        self.add_points(points)

        # add this envelope to lookup
        instrument.envelopes[name] = self

        # depth for individual targets
        self.target_depth = {}

        # add modulation for points
        self.add_point_modulation(self.data["modulation"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Point Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_point_modulation(self, data):

        import lib.interfaces.modulatable.envelope.get_modulation_envelope_points as mod_env

        # get modulation for envelope points
        mod_env.get_modulation_envelope_points(self, data)

        pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Target Depth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_target_depth(self, target, depth):

        self.target_depth[target] = depth

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Target Depth
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_target_depth(self, target):

        # try returning depth or 0 by default
        try:
            return self.target_depth[target]
        except:
            return 0

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Points
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_points(self, points):

        # go through points
        for point in points:

            # add missing values
            if len(point) < 1:
                point.append(0)
            if len(point) < 2:
                point.append(1)
            if len(point) < 3:
                point.append(0)
            if len(point) < 4:
                point.append(None)

            # add point to envelope
            self.add_point(point[0], point[1], point[2], point[3])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Point
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_point(self, time=0, level=1, curvature=1, curve=None):

        curve_inst = None

        if curve:
            curve_inst = lookup.add_curve_via_lookup(self.instrument, curve)

        # create point and append to lookup list
        self.points.append(EnvelopePoint(self, len(self.points), time, level, curvature, curve_inst))

        # check if there's currently a single point scenario
        if len(self.points) == 1:
            self.single_point = True
        else:
            self.single_point = False

        # set sustain if automatic sustain point is enabled
        if self.sustain_auto:

            if self.sustain_relative:
                self.sustain = max(len(self.points) - self.sustain - 1, 0)
            else:
                self.sustain = len(self.points) - 1

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Sustain
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_sustain(self, index):

        # set sustain within points limit and above 0
        self.sustain = max(min(index, len(self.points) - 1), 0)

        # disable automatic sustain point
        self.sustain_auto = False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        data = ""

        data += "// ::: Envelope " + str(self.index + 1) + " :::" + "\n"

        # skip if there are no points
        if len(self.points) < 1:
            return ""

        # dynamic recalcuation
        if self.dynamic:
            data += "eg" + str(self.index) + "_dynamic=1" + "\n"
        else:
            data += "eg" + str(self.index) + "_dynamic=0" + "\n"

        # go through points, add them one by one
        for idx, point in enumerate(self.points):

            # level
            data += "eg" + str(self.index) + "_level" + str(idx) + "=" + str(point.level.get()) + "\n"

            # time
            data += "eg" + str(self.index) + "_time" + str(idx) + "=" + str(point.time.get()) + "\n"

            # curvature (ignore 0 - default, linear)
            if point.curvature != 0:
                data += "eg" + str(self.index) + "_shape" + str(idx) + "=" + str(point.curvature) + "\n"

            # curve index
            if point.curve:
                data += "eg" + str(self.index) + "_curve" + str(idx) + "=" + str(point.curve.index) + "\n"

        # sustain
        if self.sustain:
            data += "eg" + str(self.index) + "_sustain=" + str(self.sustain) + " "

        # get envelope point modulation lines
        mod_lines = self.get_modulation()

        # add a linebreak when there are modulation lines available
        if mod_lines:
            data += "\n"

        mod_lines_cc = []
        mod_lines_var = []

        # filter cc lines
        for line in mod_lines:
            if "cc" in line:
                mod_lines_cc.append(line)

        # filter variable lines
        for line in mod_lines:
            if "var" in line:
                mod_lines_var.append(line)

        # print cc lines
        for line in mod_lines_cc:
            data += line + "\n"

        # print variable lines
        for line in mod_lines_var:
            data += line + "\n"

        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_modulation(self):

        # return array
        lines = []

        # go through points
        for point in self.points:

            # get line arrays from points
            lines_times = point.time.get_modulation()
            lines_levels = point.level.get_modulation()

            # expand line arrays
            for line in lines_times:
                lines.append(line)

            for line in lines_levels:
                lines.append(line)

        # return one-dimensional line array
        return lines

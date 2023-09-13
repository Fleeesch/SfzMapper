# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sfz Structure : Split
#
#   Chain of Creation:
#   Builder > Instrument > Part > Zone > [Split] > Sound
#
#   Split Section of a Zone across the Y-Axis,
#   for segementing a zone in different levels
#   that can be addressed by CC or velocity
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib import message
from lib import lookup
from lib.classes.sfz_structure.helpers.crossfade.types.class_crossfade_cc import \
    CrossfadeCC
from lib.classes.sfz_structure.helpers.crossfade.types.class_crossfade_velocity import \
    CrossfadeVelocity

from ..class_sfz_structure import SfzStructure
from ..helpers.sequence.types.class_sequence_hybrid import SequenceHybrid
from ..helpers.sequence.types.class_sequence_linear import SequenceLinear
from ..helpers.sequence.types.class_sequence_random import SequenceRandom


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Split(SfzStructure):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create Split if New
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def create_split(zone, sound):

        target_split = None

        # a split with the same level exists? use that one
        for s in zone.splits:
            if s.level == sound.level:
                target_split = s
                break

        # No split exists ? Create one!
        if target_split is None:

            # try creating a split
            try:
                target_split = Split(zone, sound.level)
            except:
                # generic error message
                message.error("Something went wrong when creating the Split")

            zone.splits.append(target_split)

        # add sample to split
        target_split.sounds.append(sound)

        # place sound in split
        sound.place_in_split(target_split)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, zone, level):

        # super constructor
        super().__init__(zone.part.instrument)

        # sounds lookup
        self.sounds = []

        # sequence container
        self.sequence = None

        # store source zone
        self.zone = zone

        # level range data
        self.level = level
        self.level_low = level
        self.level_high = level

        # y-axis crossfade data
        self.fades = {}
        self.crossfade_low_start = None
        self.crossfade_low_end = None
        self.crossfade_high_start = None
        self.crossfade_high_end = None

        # crossfade
        self.crossfade = None

        # crossfade is controlled by velocity
        self.force_full_range = False

        # load control source
        self.load_control_source()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_range(self, prefix):

        # return crossfade tag if available
        if self.crossfade:
            return str(prefix) + self.crossfade.tag_range
        else:
            # return velocity if there are no crossfades
            return str(prefix) + "vel"

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Control Source
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_control_source(self):

        # get split settings
        data = self.zone.part.map_data["splits"]

        # load crossfade control data
        data_ctrl = data["crossfade"]["control"]

        # store crossfade types
        type = data["crossfade"]["type"]
        depth = data["crossfade"]["depth"]
        source = data_ctrl["source"]

        # skip if there's no crossfading
        if not depth:
            return

        # control type - CC
        if data_ctrl["type"] == "cc":
            self.crossfade = CrossfadeCC(type, depth, source)

            # crossfade uses no velocity
            self.force_full_range = True

        # control type - Channel Aftertouch
        elif data_ctrl["type"] == "aftertouch":
            self.crossfade = CrossfadeCC(type, depth, lookup.CC_CHANNEL_AT)

            # crossfade uses no velocity
            self.force_full_range = True

        # control type - Control
        elif data_ctrl["type"] == "control":
            # pick control from instrument lookup table
            self.crossfade = CrossfadeCC(type, depth, self.instrument.controls[source].get_cc())

            # crossfade uses no velocity
            self.force_full_range = True

        # control type - Velocity
        else:
            self.crossfade = CrossfadeVelocity(type, depth)

        # force full range if settings say so
        if data["full level"] == True:
            self.force_full_range = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create Sequence
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create_sequence(self):

        # no need to create a sequence with 1 sound
        if len(self.sounds) <= 1:
            return

        # get roundrobin type
        type = self.zone.part.map_data["roundrobin"]

        # don't create sequence with only one sound
        if len(self.sounds) <= 1:
            return None

        # create sequence based on type
        if type == "random":
            self.sequence = SequenceRandom(self.sounds)
        elif type == "hybrid":
            self.sequence = SequenceHybrid(self.sounds)
        else:
            self.sequence = SequenceLinear(self.sounds)

        self.sequence.create()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Range from DataSet
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_range_from_dataset(self, fades=None):

        # don't do any crossfading when there's only one sample
        if fades is None:
            return

        # crossfade / curve transformation factors
        curve = self.zone.part.map_data["splits"]["curve"]
        cf_factor = self.zone.part.map_data["splits"]["crossfade"]["depth"]

        # level range
        range_low = fades["linear"]["low"]["start"] * cf_factor + fades["step"]["low"]["start"] * (1 - cf_factor)
        range_high = fades["linear"]["high"]["end"] * cf_factor + fades["step"]["high"]["start"] * (1 - cf_factor)

        # crossfades
        cf_low_start = fades["linear"]["low"]["start"] * cf_factor + fades["step"]["low"]["start"] * (1 - cf_factor)
        cf_low_end = fades["linear"]["low"]["end"] * cf_factor + fades["step"]["low"]["end"] * (1 - cf_factor)
        cf_high_start = fades["linear"]["high"]["start"] * cf_factor + fades["step"]["high"]["start"] * (1 - cf_factor)
        cf_high_end = fades["linear"]["high"]["end"] * cf_factor + fades["step"]["high"]["end"] * (1 - cf_factor)

        # apply curve tansformation
        range_low = pow(range_low, curve)
        range_high = pow(range_high, curve)
        cf_low_start = pow(cf_low_start, curve)
        cf_low_end = pow(cf_low_end, curve)
        cf_high_start = pow(cf_high_start, curve)
        cf_high_end = pow(cf_high_end, curve)

        # convert to 7-bit
        range_low = round(range_low * 127)
        range_high = round(range_high * 127)
        cf_low_start = round(cf_low_start * 127)
        cf_low_end = round(cf_low_end * 127)
        cf_high_start = round(cf_high_start * 127)
        cf_high_end = round(cf_high_end * 127)

        # correct potential overlap
        if cf_factor == 0 and range_low > 0:
            range_low += 1

        # store variables
        self.level_low = range_low
        self.level_high = range_high
        self.crossfade_low_start = cf_low_start
        self.crossfade_low_end = cf_low_end
        self.crossfade_high_start = cf_high_start
        self.crossfade_high_end = cf_high_end

        # disable crossfade if there's no range
        if self.crossfade_low_start == self.crossfade_low_end:
            self.crossfade_low_start = None
            self.crossfade_low_end = None

        # disable crossfade if there's no range
        if self.crossfade_high_start == self.crossfade_high_end:
            self.crossfade_high_start = None
            self.crossfade_high_end = None

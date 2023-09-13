# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sfz Structure : Zone
#
#   Chain of Creation:
#   Builder > Instrument > Part > [Zone] > Split > Sound
#
#   Tonal Segment of a Part, used for defining
#   the tonal range of samples
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.config import config

from ..class_sfz_structure import SfzStructure
from .class_split import Split


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Zone(SfzStructure):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   Static Method : Create Zone
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def create(part, sound):

        target_zone = None

        # check if zone with given note exists, pick that one instead of creating a new one
        for z in part.zones:
            if z.note == sound.note:
                target_zone = z
                break

        # no zone exists? create one
        if target_zone is None:
            target_zone = Zone(part, sound.note)

        # creating split
        Split.create_split(target_zone, sound)

        # return created / existing zone
        return target_zone

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   Constructor
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self, part, note):

        # super constructor
        super().__init__(part.instrument)

        # split lookup
        self.splits = []

        self.map_data = part.map_data["zones"]
        self.map_data = config.merge_with_defaults(self.map_data, ["zones"])

        # store attributes
        self.part = part
        self.note = note
        self.note_low = note
        self.note_high = note

        # pitch keycenter note
        self.note_center = note

        # x-axis crossfade flags representing usage
        self.use_crossfades_low = False
        self.use_crossfades_high = False
        # x-axis crossfade data
        self.crossfade_low_start = None
        self.crossfade_low_end = None
        self.crossfade_high_start = None
        self.crossfade_high_end = None

        # append to part zone lookup list
        part.zones.append(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Copy Zone Data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def copy_zone_data(self, zone):

        self.splits = zone.splits

        # store attributes
        self.part = zone.part
        self.note = zone.note
        self.note_low = zone.note
        self.note_high = zone.note

        # pitch keycenter note
        self.note_center = zone.note

        # x-axis crossfade flags representing usage
        self.use_crossfades_low = zone.use_crossfades_low
        self.use_crossfades_high = zone.use_crossfades_high
        # x-axis crossfade data
        self.crossfade_low_start = zone.crossfade_low_start
        self.crossfade_low_end = zone.crossfade_low_end
        self.crossfade_high_start = zone.crossfade_high_start
        self.crossfade_high_end = zone.crossfade_high_end

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Apply Crossfades
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~    

    def apply_crossfades(self):

        # mark low crossfades as used
        if self.crossfade_low_start != self.crossfade_low_end:
            self.use_crossfades_low = True
            # extend note range
            self.note_low = self.crossfade_low_start

        # mark high crossfades as used
        if self.crossfade_high_start != self.crossfade_high_end:
            self.use_crossfades_high = True
            # extend note range
            self.note_high = self.crossfade_high_end

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Adjust Split Levels
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def adjust_split_levels(self, reverse=False):

        lvl_max = 0

        # formatting for 1 region (skip the rest)
        if len(self.splits) <= 1:
            # spread split accross full range
            self.splits[0].force_full_range = True

            # skip
            return

        # get highest level
        for s in self.splits:
            lvl_max = max(lvl_max, s.level)

        # use highest level as reference
        lvl_min = lvl_max

        # get lowest level
        for s in self.splits:
            lvl_min = min(lvl_min, s.level)

        # adjustment factor
        factor = 1 / lvl_max

        # adjust factors
        for idx, s in enumerate(self.splits):

            if not reverse:
                s.level = s.level * factor
            else:
                s.level = (lvl_max - s.level) * factor

                # create array containing all zone notes
            arr_nr = []
            for idx, s in enumerate(self.splits):
                arr_nr.append(s.level)

            # sort zones based on numbers list
            nr_sorted, splits_sorted = (list(x) for x in
                                        zip(*sorted(zip(arr_nr, self.splits), key=lambda pair: pair[0])))

        # store sorted regions
        self.splits = splits_sorted

        # calculate vertical range / crossfades
        for idx, s in enumerate(self.splits):

            # initiate dicts
            fades = {}
            fades["step"] = {}
            fades["step"]["low"] = {}
            fades["step"]["high"] = {}
            fades["linear"] = {}
            fades["linear"]["low"] = {}
            fades["linear"]["high"] = {}
            fades["step"]["low"]["start"] = 0
            fades["step"]["low"]["end"] = 0
            fades["step"]["high"]["start"] = 0
            fades["step"]["high"]["start"] = 0
            fades["linear"]["low"]["start"] = 1
            fades["linear"]["low"]["end"] = 1
            fades["linear"]["high"]["start"] = 1
            fades["linear"]["high"]["end"] = 1

            # basic units
            unit = {}
            unit["step"] = (1.0 / len(self.splits))
            unit["linear"] = (1.0 / (len(self.splits) - 1))

            # calculate stepped ranges
            fades["step"]["low"]["start"] = unit["step"] * idx
            fades["step"]["low"]["end"] = fades["step"]["low"]["start"]
            fades["step"]["high"]["start"] = unit["step"] * (idx + 1)
            fades["step"]["high"]["end"] = fades["step"]["high"]["start"]

            # calculate crossfade zones
            fades["linear"]["low"]["start"] = unit["linear"] * (idx - 1)
            fades["linear"]["low"]["end"] = unit["linear"] * idx
            fades["linear"]["high"]["start"] = fades["linear"]["low"]["end"]
            fades["linear"]["high"]["end"] = unit["linear"] * (idx + 1)

            # crossfade exception for lowest region
            if idx == 0:
                fades["linear"]["low"]["start"] = 0
                fades["linear"]["low"]["end"] = 0
                fades["linear"]["high"]["start"] = 0
                fades["linear"]["high"]["end"] = unit["linear"] * (idx + 1)

            # crossfade exception for highest region
            if idx == len(self.splits) - 1:
                fades["linear"]["low"]["start"] = unit["linear"] * (idx - 1)
                fades["linear"]["low"]["end"] = 1
                fades["linear"]["high"]["start"] = 1
                fades["linear"]["high"]["end"] = 1

            # transfader calculated data to region
            s.set_range_from_dataset(fades)

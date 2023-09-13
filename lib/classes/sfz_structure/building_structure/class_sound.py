# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sfz Structure : Sound
#
#   Chain of Creation:
#   Builder > Instrument > Part > Zone > Split > [Sound]
#
#   Last building block in the chain of creation,
#   contains samples and their attributes
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os

import lib.classes.sfz_structure.group.class_group as group
from lib.config import config

from ..class_sfz_structure import SfzStructure


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Sound(SfzStructure):
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    lookup = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Get Sample List
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sample_list(path):

        if not os.path.exists(path):
            return None

        samples = []

        for f in os.scandir(path):
            file_str = os.path.basename(f)
            samples.append(file_str)

        return samples

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, part, file, name, note, level, roundrobin=0):

        # super constructor
        super().__init__(part.instrument)

        # store attributes
        self.part = part
        self.file = file
        self.name = name
        self.note = note
        self.level = level
        self.roundrobin = roundrobin

        # alternative keycenter
        self.keycenter = note

        # data
        self.map_data = self.part.map_data["sounds"]
        self.map_data = config.merge_with_defaults(self.map_data, "sounds")

        # if sound  belongs to sequence
        self.sequence = None

        # split placement
        self.split = None

        # random settings
        self.use_random = False
        self.random_low = 0
        self.random_high = 1

        # sequence settings
        self.use_sequence = False
        self.sequence_length = 0
        self.sequence_position = 0

        # pitch keytrack
        self.keytrack = 100
        self.store_keytrack_from_settings()

        # load attributes
        self.load_attributes(self.map_data)

        # load settings
        self.load_settings(self.map_data)

        # load group settings
        # -> only if part is not hidden to prevent group number overshoot
        if not self.part.hide:
            self.load_group_settings()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Store Keytrack from Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def store_keytrack_from_settings(self):

        for setting in self.settings:
            if setting.tag == "pitch_keytrack":
                self.keytrack = setting.value

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add to Sequence
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_to_sequence(self, sequence):
        sequence.add_sound(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Keycenter
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_keycenter(self, note):
        self.keycenter = note

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Place in Split
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def place_in_split(self, split):
        self.split = split

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Round Robin
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_roundrobin(self, index):
        self.roundrobin = index

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Center Note
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_center_note(self, note):
        self.set_center_note = note

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Sample Location
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sample_location(self):
        return self.file.get_full_path_relative(self.instrument)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sequence : Hybrid
#
#   Combination of sequence and random Roundrobin,
#   splits the samples into two groups of samples
#   that alternate between each other.
#
#   Samples within the group use randomized playback.
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
from ..class_sequence import Sequence

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SequenceHybrid(Sequence):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Create Sequence
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, sounds):

        super().__init__(sounds)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create(self):

        # super method
        super().create()

        # hybrid needs at least 3 sounds, return to sequence if less are found
        if len(self.sounds) < 3:
            return

        split = round(len(self.sounds) / 2 - 0.5)

        for i, sound in enumerate(self.sounds):

            sound.use_sequence = True
            sound.sequence_length = 2

            # split A
            if i < split:
                # sequence position
                seq_pos = 1
                # sound count of section
                section_count = split
                # last index position of secion
                max_pos = split - 1
                # sound index with section offset
                idx = i

            # split B
            else:
                # sequence position
                seq_pos = 2
                # sound count of section
                section_count = len(self.sounds) - split
                # last index position of secion
                max_pos = len(self.sounds) - 1
                # sound index with section offset
                idx = i - split

            # store sequence position
            sound.sequence_position = seq_pos

            # calculate random section
            rand_section = 1 / section_count

            # random posibility low and high
            rand_low = idx * rand_section
            rand_high = rand_low + rand_section

            # trim random ceiling to prevent potential overlap
            rand_high -= 0.000000001

            # last random section is always hitting the ceiling
            if i >= max_pos:
                rand_high = 1

            # store random bounds
            if not (rand_low == 0 and rand_high == 1):
                sound.use_random = True
                sound.random_low = rand_low
                sound.random_high = rand_high

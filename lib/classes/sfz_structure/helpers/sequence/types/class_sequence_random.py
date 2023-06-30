# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sequence : Random
#
#   Randomized Roundrobin
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


class SequenceRandom(Sequence):

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

        # calculate random section
        rand_section = 1 / len(self.sounds)

        # go through sounds
        for idx, sound in enumerate(self.sounds):

            # sound uses random
            sound.use_random = True

            # calcualte random borders
            rand_low = idx * rand_section
            rand_high = rand_low + rand_section

            # add slight offset in random high border to prevent overlap
            rand_high -= 0.000000001

            # last sound has always the topmost random high level
            if idx >= len(self.sounds) - 1:
                rand_high = 1

            # store data in sound
            sound.random_low = rand_low
            sound.random_high = rand_high

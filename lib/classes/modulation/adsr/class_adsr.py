# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : ADSR
#
#   Represents a SFZ1 ADSR envelope
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.modulation.adsr.elements.class_adsr_element_attack import \
    AdsrElementAttack
from lib.classes.modulation.adsr.elements.class_adsr_element_decay import \
    AdsrElementDecay
from lib.classes.modulation.adsr.elements.class_adsr_element_delay import \
    AdsrElementDelay
from lib.classes.modulation.adsr.elements.class_adsr_element_hold import \
    AdsrElementHold
from lib.classes.modulation.adsr.elements.class_adsr_element_release import \
    AdsrElementRelease
from lib.classes.modulation.adsr.elements.class_adsr_element_sustain import \
    AdsrElementSustain

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Adsr():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, source, tag=""):

        # store attributes
        self.source = source
        self.instrument = source.instrument
        self.tag = tag

        # setup basic adsr structure
        self.delay = AdsrElementDelay(self)
        self.attack = AdsrElementAttack(self)
        self.hold = AdsrElementHold(self)
        self.decay = AdsrElementDecay(self)
        self.sustain = AdsrElementSustain(self)
        self.release = AdsrElementRelease(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_modulation(self, data):

        # load modulations for individual adsr elements
        self.delay.load_modulation(data["delay"])
        self.attack.load_modulation(data["attack"])
        self.hold.load_modulation(data["hold"])
        self.decay.load_modulation(data["decay"])
        self.sustain.load_modulation(data["sustain"])
        self.release.load_modulation(data["release"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Modulation SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_modulation(self):

        # loaded line arrays
        line_set = []

        # get line arrays from modulations
        line_set.append(self.delay.value.get_modulation())
        line_set.append(self.attack.value.get_modulation())
        line_set.append(self.hold.value.get_modulation())
        line_set.append(self.decay.value.get_modulation())
        line_set.append(self.sustain.value.get_modulation())
        line_set.append(self.release.value.get_modulation())
        
        # return array
        lines = []

        # go through lines, collect them
        for set in line_set:
            for line in set:
                lines.append(line)

        # return modulation line array
        return lines

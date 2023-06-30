# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : AmpEG
#
#   Amplitude Envelope of a SFZ Structure
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.audio_processor.class_audio_processor import AudioProcessor
from lib.classes.modulation.adsr.class_adsr import Adsr

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class AmpEg(AudioProcessor):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, source, data):
        
        # super constructor
        super().__init__(source)

        # store data
        self.data = data

        # create adsr
        self.adsr = Adsr(self, "ampeg")

        # dynamic recalculation
        self.dynamic = False

        # load settings
        self.load_settings()

        # load adsr elements from data
        self.load_adsr_from_data()

        # load value modulation for adsr elements
        self.load_modulation()

        # link to source
        source.ampeg = self

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_settings(self):

        # dynamic recalculation is either 1 or 0
        if self.data["dynamic"]:
            self.dynamic = self.dynamic = 1
        else:
            self.dynamic = self.dynamic = 0

        pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load ADSR from Data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_adsr_from_data(self):

        # setup delay
        self.adsr.delay.set_value(self.data["delay"]["level"])

        # setup attack
        self.adsr.attack.set_value(self.data["attack"]["level"])
        self.adsr.attack.set_shape(self.data["attack"]["shape"])

        # setup hold
        self.adsr.hold.set_value(self.data["hold"]["level"])
        
        # setup decay
        self.adsr.decay.set_value(self.data["decay"]["level"])
        self.adsr.decay.set_shape(self.data["decay"]["shape"])

        # setup sustain
        self.adsr.sustain.set_value(self.data["sustain"]["level"])

        # setup release
        self.adsr.release.set_value(self.data["release"]["level"])
        self.adsr.release.set_shape(self.data["release"]["shape"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_modulation(self):
        self.adsr.load_modulation(self.data)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        # return string
        data = ""

        # dynamic recalculation
        data += "ampeg_dynamic=" + str(self.dynamic) + "\n"

        # delay
        data += "ampeg_delay=" + str(self.adsr.delay.get_value() + self.adsr.delay.value.calculate_compensation()) + "\n"
        
        # attack
        data += "ampeg_attack=" + str(self.adsr.attack.get_value() + self.adsr.attack.value.calculate_compensation()) + "\n"
        
        # attack shape
        if self.adsr.attack.get_shape() != 0:
            data += "ampeg_attack_shape=" + str(self.adsr.attack.get_shape()) + "\n"
        
        # hold
        data += "ampeg_hold=" + str(self.adsr.hold.get_value() + self.adsr.hold.value.calculate_compensation()) + "\n"
        
        # decay
        data += "ampeg_decay=" + str(self.adsr.decay.get_value() + self.adsr.decay.value.calculate_compensation()) + "\n"
        
        # decay shape
        if self.adsr.decay.get_shape() != 0:
            data += "ampeg_decay_shape=" + str(self.adsr.decay.get_shape()) + "\n"
        
        # sustain
        data += "ampeg_sustain=" + str(self.adsr.sustain.get_value() + self.adsr.sustain.value.calculate_compensation()) + "\n"
        
        # release
        data += "ampeg_release=" + str(self.adsr.release.get_value() + self.adsr.release.value.calculate_compensation()) + "\n"
        
        # release shape
        if self.adsr.release.get_shape() != 0:
            data += "ampeg_release_shape=" + str(self.adsr.release.get_shape()) + "\n"
        
        # add adsr modulation
        mod_lines = self.adsr.get_sfz_modulation()
        
        # add mod lines to return array
        for line in mod_lines:
            data += line + "\n"
        
        # return sfz string
        return data

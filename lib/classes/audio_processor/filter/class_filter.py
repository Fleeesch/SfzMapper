# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Filter
#
#   Represents a filter that is supported
#   by the SFZ structure
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import copy

from lib import lookup
from lib.classes.audio_processor.filter.element.class_filter_frequency import \
    FilterFrequency
from lib.classes.audio_processor.filter.element.class_filter_gain import \
    FilterGain
from lib.classes.audio_processor.filter.element.class_filter_resonance import \
    FilterResonance
from lib.config import config

from ..class_audio_processor import AudioProcessor

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Filter(AudioProcessor):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Copy Filter
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def copy_filter(source, filter_name):

        try:

            # get original filter from instrument filter pool
            org_fil = source.instrument.filters[filter_name]
            
            # create new filter instance linked to source
            fil_new = Filter(source, org_fil)
            
            # copy attributes
            fil_new.type = org_fil.type
            fil_new.type.poles = org_fil.type.poles
            
            fil_new.frequency.depth = org_fil.frequency.depth
            fil_new.resonance.depth = org_fil.resonance.depth
            fil_new.gain.depth = org_fil.gain.depth
            
            fil_new.keytrack = org_fil.keytrack
            fil_new.keytrack_center = org_fil.keytrack_center
            fil_new.velocity_track = org_fil.velocity_track
            
            # return created filter
            return fil_new
        except:
            # return nothing on fail
            return None
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, source, original_filter=None):
        
        # super constructor
        super().__init__(source)
        
        # store original filter reference
        self.original_filter = original_filter
        
        # setup attributes
        self.frequency = FilterFrequency(self)
        self.resonance = FilterResonance(self)
        self.gain = FilterGain(self)

        # keytracking
        self.keytrack = 0

        # keytracking center
        self.keytrack_center = 64

        # velocity tracking
        self.velocity_track = 0

        # filter index
        self.index = 0

        # type is undeclared at the beginning
        self.type = None

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_modulation(self, data):

        # go through modulation targets
        for mod_target in data:

            # go through modulation types of target
            for mod_type in data[mod_target]:

                if mod_type == "type":
                    continue

                if data[mod_target][mod_type] is None:
                    continue

                # go through modulations
                for mod in data[mod_target][mod_type]:

                    # merge modulation section with defaults
                    data[mod_target][mod_type][mod] = config.merge_with_defaults(data[mod_target][mod_type][mod], "modulation element")

        # add modulation to sections
        self.frequency.add_modulation(data["frequency"])
        self.resonance.add_modulation(data["resonance"])
        self.gain.add_modulation(data["gain"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        # return string
        data = ""

        # 1st filter suffix (there is none)
        idx = ""

        # 2nd filter suffix
        if self.index >= 2:
            idx = "2"

        # type (differentiate between pole and non-pole filters)
        if self.type.poles_lookup is None:
            data += "fil" + idx + "type=" + self.type.tag + "\n"
        else:
            data += "fil" + idx + "type=" + self.type.tag + "_" + str(self.type.poles) + "p" + "\n"
        
        # cutoff
        data += self.frequency.tag + idx + "=" + str(self.frequency.depth + self.frequency.calculate_compensation()) + "\n"
        
        # resonance
        data += self.resonance.tag + idx + "=" + str(self.resonance.depth + self.resonance.calculate_compensation()) + "\n"
        
        # gain
        data += "fil" + idx + "_" + self.gain.tag + "=" + str(self.gain.depth + self.gain.calculate_compensation()) + "\n"
        
        # keytracking
        data += "fil" + idx + "_keytrack=" + str(self.keytrack) + "\n"
        
        # keytracking center
        data += "fil" + idx + "_keycenter=" + str(self.keytrack_center) + "\n"
        
        # velocity tracking
        data += "fil" + idx + "_veltrack=" + str(self.velocity_track) + "\n"
        
        # modulation
        freq_lines = self.frequency.get_modulation()
        resonance_lines = self.resonance.get_modulation()
        gain_lines = self.gain.get_modulation()
        
        # add frequency modulation lines
        for line in freq_lines:
            data += line + "\n"
        
        # add resonance modulation lines
        for line in resonance_lines:
            data += line + "\n"
        
        # add gain modulation lines
        for line in gain_lines:
            data += "fil" + idx + "_" + line + "\n"
        
        # return sfz string
        return data
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Type
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def set_type(self, type_string, poles):
        
        # only set type once
        if self.type:
            return

        try:
            # get class reference via lookup
            filter_class = lookup.FILTER_LOOKUP[type_string]
            # create instance of filter type
            self.type = filter_class(self)
            self.type.set_poles(poles)
        except:
            pass

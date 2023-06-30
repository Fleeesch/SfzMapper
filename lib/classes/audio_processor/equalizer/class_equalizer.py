# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Audio Processor : Equalizer
#
#   A Container for a maxmimum of 3 Equalizer Bands
#   that the SFZ standard allows per voice
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import copy

from lib.classes.audio_processor.equalizer.element.class_equalizer_band import \
    EqualizerBand
from lib.config.reformat import reformat_modulation_attribute as ref_att

from ..class_audio_processor import AudioProcessor

from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Equalizer(AudioProcessor):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Copy Filter
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def copy_equalizer(source, eq_name):

        try:

            # get original filter from instrument filter pool
            org_eq = source.instrument.equalizers[eq_name]

            # create new filter instance linked to source
            eq_new = Equalizer(source)

            # copy attributes
            for band in org_eq.bands:
            
                band_new = EqualizerBand(eq_new, band.index)
                band_new.frequency.depth = band.frequency.depth
                band_new.gain.depth = band.gain.depth
                band_new.bandwidth.depth = band.bandwidth.depth
            
                eq_new.bands.append(band_new)
                
            
            eq_new.band_index = org_eq.band_index

            # return created filter
            return eq_new
        except:
            # return nothing on fail
            return None

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, source):

        # super constructor
        super().__init__(source)

        # band index (starts at 1 for sfz syntax)
        self.band_index = 1

        # dynamic recalculation
        self.dynamic = False

        # bands
        self.bands = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Band
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_band(self, frequency, gain, bandwidth):

        # equalizers are limited to 3 bands
        if len(self.bands) >= 3:
            return

        # create band
        band = EqualizerBand(self, self.band_index)

        # set band attributes
        band.frequency.depth = frequency
        band.gain.depth = gain
        band.bandwidth.depth = bandwidth
        
        # append band to list
        self.bands.append(band)

        # increment band index
        self.band_index += 1

        # return band
        return band

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Modulation
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_modulation(self, data):

        for idx, band in enumerate(data):

            # only process existing bands
            if idx >= len(self.bands):
                break
            
            # merge band modulation with defaults
            data[band] = config.merge_with_defaults(data[band], "equalizer band modulation")
            
            # reformat modulation sections
            data[band]["frequency"] = ref_att.reformat_modulation_attribute(data[band]["frequency"])
            data[band]["gain"] = ref_att.reformat_modulation_attribute(data[band]["gain"])
            data[band]["bandwidth"] = ref_att.reformat_modulation_attribute(data[band]["bandwidth"])

            # store modulation data
            mod_data = data[band]

            # store modulatable element data
            mod_freq = mod_data["frequency"]
            mod_gain = mod_data["gain"]
            mod_bandwidth = mod_data["bandwidth"]

            # add modulation to band attributes
            self.bands[idx].frequency.add_modulation(mod_freq)
            self.bands[idx].gain.add_modulation(mod_gain)
            self.bands[idx].bandwidth.add_modulation(mod_bandwidth)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        # sfz return array
        data = ""

        # go through bands, add sfz
        for band in self.bands:

            # [!] dynamic seems to be unsupported in ARIA
            # if self.dynamic:
            #    data += band.tag + "_dynamic=1" + "\n"
            # else:
            #    data += band.tag + "_dynamic=0" + "\n"

            data += band.get_sfz()

        # return sfz string
        return data

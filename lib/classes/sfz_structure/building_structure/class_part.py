# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sfz Structure : Part
#
#   Chain of Creation:
#   Builder > Instrument > [Part] > Zone > Split > Sound
#
#   Represents a part of an instrument,
#   used for spreading shared attributes accross
#   the sounds it contains and for
#   making keyswitches / grouping manageable
#
#   Most of the mapping process is happening here.
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from copy import deepcopy
import fnmatch
import math

from lib.classes.sfz_structure.building_structure.class_generator import Generator


from lib import message

from lib import functions as func
from lib.classes.class_file import File
from lib.classes.sfz_structure.class_sfz_structure import SfzStructure
from lib.classes.sfz_structure.helpers.crossfade.types.class_crossfade_tonal import \
    CrossfadeTonal
from lib.config import config

from .class_sound import Sound
from .class_zone import Zone

from lib.classes.sfz_structure.group.class_group import Group

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Part(SfzStructure):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    lookup = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Create
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def create(instrument, name, map_data):
        
        # create instance
        part = Part(instrument, name, map_data)
        
        # store into lookup
        Part.lookup.append(part)
        
        # store into builder lookup
        instrument.parts[name] = part
        
        return part
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, instrument, name, map_data):

        # super constructor
        super().__init__(instrument)

        # store attributes
        self.name = name

        # load data and merge with defaults
        self.map_data = map_data
        self.map_data = config.merge_with_defaults(self.map_data, "parts")
        self.map_data["zones"] = config.merge_with_defaults(self.map_data["zones"], "zones")
        self.map_data["splits"] = config.merge_with_defaults(self.map_data["splits"], "splits")
        self.map_data["sounds"] = config.merge_with_defaults(self.map_data["sounds"], "sounds")
        self.map_data["samples"] = config.merge_with_defaults(self.map_data["samples"], "samples")

        # hide flag
        self.hide = self.map_data["hide"]

        # get sample location
        self.samples_path = self.instrument.builder.map_path + "/" + self.map_data["samples"]["location"]

        # zones
        self.zones = []
        self.crossfade = None
        self.load_crossfade_settings()

        self.tonal_fade_type = None

        # samples
        self.samples = []

        # get samples list
        self.samples = Sound.get_sample_list(self.samples_path)

        # get keyrange
        self.keyrange_low = self.map_data["keyrange"]["low"]
        self.keyrange_high = self.map_data["keyrange"]["high"]

        # skip if there are no samples found
        if self.samples is None:
            raise Exception

        # reverse playback flag
        # [!] Reverse has to be implemented as a non-attribute,
        #     since ARIA requires the reverse flag to be placed within <region> headers

        self.reverse = False
        self.load_reverse_setting()

        # load filters
        self.load_local_filters()

        # load equalizer
        self.load_local_equalizer()


        # try mapping a generator first, continue with samples on fail
        try:
            if not self.map_generator():
                self.map_samples()
        except:
            # generic error message
            message.error("Something went when trying to map the Samples")

        # load group settings
        self.load_group_settings()

        # load attributes
        self.load_attributes(self.map_data)

        # load keyswitches
        self.load_keyswitch()

        # load keyrange bypass setting
        self.load_keyrange_bypass()

        # load pedal settings
        self.load_pedal_settings()

        # load cc range
        self.load_cc_range()

        # load cc range trigger
        self.load_cc_range_trigger()

        # load program change range
        self.load_program_range()

        # load settings
        self.load_settings(self.map_data)

        # load amp EG
        self.load_amp_eg()

        # load release envelope
        self.load_release_envelope()

        # load includes
        self.load_includes()

        # load pitchbend settings
        self.load_pitchbend_settings()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Settings SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_part(self):

        data = ""

        # load crossfade settings if crossfade exists
        if self.crossfade:
            data += self.crossfade.get_sfz()

        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Reverse Playback Setting
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_reverse_setting(self):

        # anything true value will turn on reverse playback
        if self.map_data["reverse"]:
            self.reverse = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Crossfade
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_crossfade_settings(self):

        # load data
        type = self.map_data["zones"]["crossfade"]["type"]
        depth = self.map_data["zones"]["crossfade"]["depth"]

        # create tonal part crossfade if depth is not zero
        if depth:
            self.crossfade = CrossfadeTonal(type, depth)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Index Round Robins
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def setup_sequences(self):

        for zone in self.zones:
            for split in zone.splits:
                split.create_sequence()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Apply Polymono
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def apply_polymono(self):

        # skip if polymono is off
        if not self.group_polymono:
            return

        # copy zone list
        zone_list = self.zones

        # empty zone list
        self.zones = []

        # go through zones
        for idx, zone in enumerate(zone_list):

            # go trhough note range of zone
            for note in range(zone.note_low, zone.note_high + 1):

                # create new zone
                zone_new = Zone(self, note)

                # copy original zone data
                zone_new.copy_zone_data(zone)

                # rescale note data
                zone_new.note = note
                zone_new.note_low = note
                zone_new.note_high = note

                # create zone-exclusive choke group
                group = Group.add_group_to_instrument(zone_new, "Choke:" + str(id(zone_new)))

                # transfer group info to zone
                zone_new.group = group
                zone_new.group_off = group

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Adjust all Zone Levels
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def adjust_all_zone_levels(self):

        # get reverse setting
        reverse = self.map_data["samples"]["mapping"]["level"]["reverse"]

        # adjust levels, reverse optionally
        for z in self.zones:
            z.adjust_split_levels(reverse)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Sort Sounds By Note
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def sort_sounds_by_note(self, sounds):

        # skip if there's nothing to process
        if (len(sounds) <= 0):
            return sounds

        # create array containing all zone notes
        arr_nr = []

        for idx, snd in enumerate(sounds):
            arr_nr.append(snd.note)

        # sort zones based on numbers list
        nr_sorted, sounds_sorted = (list(x) for x in zip(*sorted(zip(arr_nr, sounds), key=lambda pair: pair[0])))

        # store ordered zones
        return sounds_sorted

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Sort Zones By Note
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def sort_zones_by_note(self):

        if (len(self.zones) <= 0):
            return

        # create array containing all zone notes
        arr_nr = []

        for idx, z in enumerate(self.zones):
            arr_nr.append(z.note)

        # sort zones based on numbers list
        nr_sorted, zones_sorted = (list(x) for x in zip(*sorted(zip(arr_nr, self.zones), key=lambda pair: pair[0])))

        # store ordered zones
        self.zones = zones_sorted

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Crossfade Zones
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def crossfade_zones(self):

        # go through zones
        for idx, z in enumerate(self.zones):

            # skip if crossfade is not available
            if not self.crossfade:
                continue

            # get previous and next zones
            prev = self.zones[max(idx - 1, 0)]
            next = self.zones[min(idx + 1, len(self.zones) - 1)]

            # assume single note
            note_low = z.note
            note_high = z.note

            # store delta of neighbour notes
            dif_low = z.note - prev.note
            dif_next = next.note - z.note

            # store previous note edge if usable
            if abs(dif_low) > 1:
                note_low = prev.note + 1

            # next previous note edge if usable
            if abs(dif_next) > 1:
                note_high = next.note - 1

            # get crossfade depth
            crossfade = self.crossfade.depth

            # calculate note edges based on crossfade factor
            cf_note_low = math.floor(z.note_low * (1 - crossfade) + (note_low * crossfade))
            cf_note_high = math.ceil(z.note_high * (1 - crossfade) + (note_high * crossfade))

            # crossfade valid?
            if cf_note_low != cf_note_high:

                # low crossfade (ignore first note)
                if idx > 0:
                    z.crossfade_low_start = cf_note_low
                    z.crossfade_low_end = z.note_low

                # high crossfade (ignore last note)
                if idx < len(self.zones) - 1:
                    z.crossfade_high_start = z.note_high
                    z.crossfade_high_end = cf_note_high

        # apply crossfades, extending the zones note range
        for z in self.zones:
            z.apply_crossfades()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Spread Zones Tonal Range (Atonal)
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def spread_zones_tonal_range_atonal(self, step):

        # forced note setting
        force_note = self.map_data["keyrange"]["force note"]

        for idx, z in enumerate(self.zones):

            # get previous and next zones
            prev = self.zones[max(idx - 1, 0)]
            next = self.zones[min(idx + 1, len(self.zones) - 1)]

            # always use the base note for lowest note
            note_low = z.note_low

            if force_note:

                # pick range from list
                if type(force_note) is list:
                    note_low = force_note[0]
                    note_high = force_note[1]
                else:
                    # use single note
                    note_low = force_note
                    note_high = force_note

            # highest note gets a different treadment
            if idx >= len(self.zones) - 1:
                # extend note via step range
                note_high = note_low + (step - 1)
            else:
                # use next note as reference
                note_high = next.note_low - 1

            # limit keys to part keyrange
            note_low = max(self.keyrange_low, note_low)
            note_high = min(self.keyrange_high, note_high)

            # store note ranges in zone
            z.note_low = note_low
            z.note_high = note_high

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Spread Zones Tonal Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def spread_zones_tonal_range(self):

        # get keyrange extension
        keyrange_extend_low = self.map_data["keyrange"]["extend"]["low"]
        keyrange_extend_high = self.map_data["keyrange"]["extend"]["high"]

        # forced note setting
        force_note = self.map_data["keyrange"]["force note"]

        # go through zones (x -axis / pitch)
        for idx, z in enumerate(self.zones):

            # get previous and next zones
            prev = self.zones[max(idx - 1, 0)]
            next = self.zones[min(idx + 1, len(self.zones) - 1)]

            # get semitone delta between zone neighbours
            dif_low = prev.note - z.note
            dif_high = next.note - z.note

            # calculate low and high note boundaries
            note_low = math.ceil(z.note + (dif_low / 2.0))
            note_high = math.floor(z.note + (dif_high / 2.0))

            # overwrite note range if forced
            if force_note:

                # pick range from list
                if type(force_note) is list:
                    note_low = force_note[0]
                    note_high = force_note[1]
                else:
                    # use single note
                    note_low = force_note
                    note_high = force_note

            if idx == 0:
                note_low -= keyrange_extend_low

            if idx >= len(self.zones) - 1:
                note_high += keyrange_extend_high

            # limit keys to part keyrange
            note_low = max(self.keyrange_low, note_low)
            note_high = min(self.keyrange_high, note_high)

            # store note ranges in zone
            z.note_low = note_low
            z.note_high = note_high

            # increment lowest note if there's overlap
            # (ignore first note since it doesn't have a previous neighbour)
            if idx > 0 and prev.note_high == z.note_low:
                z.note_low += 1

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Level
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_level(self, input):

        # get pattern from configuration
        pattern = self.map_data["samples"]["mapping"]["level"]["pattern"]

        # assume full level
        level = 127

        # >> pattern is None means default
        if pattern is None:

            # filter number from level string
            level = func.filter_number(input)

        # >> pattern is an array
        elif type(pattern) is list:

            # go through pattern, find a matching pair
            for idx, i in enumerate(pattern):
                if input == i:
                    level = idx
                    break

        # >> pattern is a template reference
        else:
            pattern_ar = config.TEMPLATES["pattern"]["level"][pattern]

            # go through pattern, find a matching pair
            for idx, i in enumerate(pattern_ar):
                if input == i:
                    level = idx
                    break

        # always return level
        return level

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Note Number
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_note_number(self, nr):

        # load pattern from settings
        mapping_type = self.map_data["samples"]["mapping"]["note"]["detection"]["type"]
        pattern = self.map_data["samples"]["mapping"]["note"]["detection"]["pattern"]

        # filter string and number
        note_name = func.filter_string(nr)
        note_octave = func.filter_number(nr)

        # note by default
        note = 0

        # ::: Mappping Type - Direct :::

        if mapping_type == "direct":

            # grab number directly
            note = note_octave

        # ::: Mappping Type - Array :::

        if mapping_type == "list":

            # >> pattern is None loads a specific template by default
            if pattern is None:

                # hard coded defauld pattern
                pattern_ar = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]

                # go through pattern, check for matching pair
                for idx, i in enumerate(pattern_ar):
                    if note_name == i:
                        note = idx
                        break

            # >> check if pattern is an array
            elif type(pattern) is list:

                # go through pattern, check for matching pair
                for idx, i in enumerate(pattern):
                    if note_name.lower() == i.lower():
                        note = idx
                        break

            # >> pattern is a template reference
            else:

                # load classic template by default
                pattern_ar = config.TEMPLATES["pattern"]["tonal"][pattern]

                # go through pattern, check for matching pair
                for idx, i in enumerate(pattern_ar):
                    if note_name.lower() == i.lower():
                        note = idx
                        break

            # calculate note number by adding octave offset
            note += note_octave * 12

        # limit note to midi range
        note = min(max(note, 0), 127)

        # always return a note
        return note

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Map Generator
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def map_generator(self):

        # try setting up a generator
        try:

            # check if generator contains something
            if self.map_data["generator"]:

                # store data link
                data = self.map_data["generator"]

                # merge data with defaults
                data = config.merge_with_defaults(data, "generator")

                # type
                gen_type = data["type"]

                # note
                note = data["note"]

                # key range
                key_low = data["range"]["key"]["low"]
                key_high = data["range"]["key"]["high"]
                key_part = data["range"]["key"]["part"]

                # level range
                level_low = data["range"]["level"]["low"]
                level_high = data["range"]["level"]["high"]

                # part has been given?
                if key_part:

                    # go through instrument parts
                    for p_name in self.instrument.parts:

                        # check if name matches
                        if p_name == key_part:

                            # declare boundaries
                            key_min = 127
                            key_max = 0

                            # go through part zones
                            for z in self.instrument.parts[p_name].zones:

                                # readjust boundaries
                                key_min = min(key_min, z.note_low)
                                key_max = max(key_max, z.note_high)

                            # copy keyrange
                            key_low = key_min
                            key_high = key_max

                            # copy done
                            break

                # create generator
                gen = Generator(self, gen_type, note)

                # create zone with generator, constructing a structure
                z = Zone.create(self, gen)

                # manually change zone note range
                z.note_low = key_low
                z.note_high = key_high

                # manually change zone split level range
                z.splits[0].level_low = level_low
                z.splits[0].level_high = level_high

                # generator built successfully
                return True

        except:
            # return failed attempt
            return False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Transform Filename
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def transform_filename(self, filename):

        settings_remove = self.map_data["samples"]["edit"]["remove"]
        settings_replace = self.map_data["samples"]["edit"]["replace"]
        settings_insert = self.map_data["samples"]["edit"]["insert"]

        # remove characters from beginning
        if settings_remove["start"]:
            filename = filename[settings_remove["start"]:]

        # remove characters from end
        if settings_remove["end"]:
            filename = filename[:-settings_remove["end"]]

        # remove parts of string
        if settings_remove["string"]:

            # always transform to string list
            if type(settings_remove["string"]) is not list:
                settings_remove["string"] = [settings_remove["string"]]

            # remove strings
            for s in settings_remove["string"]:
                filename = filename.replace(s, "")

        # replace part of string
        if settings_replace["original"] and settings_replace["new"]:
            filename = filename.replace(settings_replace["original"], settings_replace["new"])

        # insert text at start
        if settings_insert["start"]:
            filename = settings_insert["start"] + filename

        # insert text at end
        if settings_insert["end"]:
            filename = filename + settings_insert["end"]

        # return changed string
        return filename

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Map Samples
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def map_samples(self):

        # mapping type
        mapping_type = self.map_data["samples"]["mapping"]["type"]

        # note step (tonal distance between samples)
        mapping_step = self.map_data["samples"]["mapping"]["note"]["incremental step"]

        # note start (beginning note from left to right)
        mapping_start = self.map_data["samples"]["mapping"]["note"]["incremental start"]

        # previous note name (comparison control mapping index)
        mapping_previous_name = ""

        # step mapping position
        mapping_index = 0

        # load filters
        f_include = self.map_data["samples"]["include"]
        f_exclude = self.map_data["samples"]["exclude"]

        # : : : : : : : : : : : : : : :
        # Analysis

        sounds = []

        # go through samples
        for smp in self.samples:

            smp_file = File(self.samples_path, smp)

            filepath_abs = smp_file.get_full_path()
            filename = smp_file.get_no_extension()
            filename_cut = self.transform_filename(filename)

            # skip indicator for filter
            skip = False

            # ::: Inclusion :::

            if isinstance(f_include, list):
                for e in f_include:
                    if not fnmatch.fnmatch(filename, e):
                        skip = True
                        break
            else:
                if not fnmatch.fnmatch(filename, f_include):
                    skip = True

            # ::: Exclusion :::

            if isinstance(f_exclude, list):
                for e in f_exclude:
                    if fnmatch.fnmatch(filename, e):
                        skip = True
                        break
            else:
                if fnmatch.fnmatch(filename, f_exclude):
                    skip = True

            # skip if filter is applied
            if skip:
                continue

            # prepare filename if multiple split symbols are given
            if type(self.map_data["samples"]["split"]) is list:

                # get first split symbol
                split_smb_first = self.map_data["samples"]["split"][0]

                # go through split symbols
                for s in self.map_data["samples"]["split"]:

                    # replace split symbol with first split symbol
                    filename_cut = filename_cut.replace(s, split_smb_first)

                # replace split symbol list with first symbol
                self.map_data["samples"]["split"] = split_smb_first

            # split filename into attributes
            data = filename_cut.split(self.map_data["samples"]["split"])

            # get naming pattern
            pattern = self.map_data["samples"]["pattern"]

            # get note shift
            note_shift = self.map_data["note shift"]

            # declare default attributes
            name = "Zone"
            level = 127
            roundrobin = 0

            # note is calculated
            note = mapping_start + mapping_step * mapping_index

            # store attributes in variables
            for idx, i in enumerate(data):

                # don't exceed pattern length
                if idx > len(pattern) - 1:
                    break

                # name
                if pattern[idx] == "name":
                    # store name
                    name = i
                    # increment mapping index if name changes
                    # (ignore empty name, being the first name)
                    if mapping_previous_name and mapping_previous_name != name:

                        # increment index, recalculate note
                        mapping_index += 1
                        note = mapping_start + mapping_step * mapping_index

                    mapping_previous_name = name
                    continue

                # level
                if pattern[idx] == "level":
                    level = self.get_level(i)
                    continue

                # roundrobin
                if pattern[idx] == "roundrobin":
                    roundrobin = func.filter_number(i)

                    continue

                # mapping type needs to be tonal
                if mapping_type == "tonal":

                    # note
                    if pattern[idx] == "note":
                        note = self.get_note_number(i)
                        continue

            # add note offset
            note = min(max(note + note_shift, 0), 127)

            # : : : : : : : : : : : : : : :
            # Sound Creation

            try:
                # create sound
                sound = Sound(self, smp_file, name, note, level, roundrobin)

                # append created sound to list
                sounds.append(sound)

            except:
                message.error("Something went wrong when creating the Sound\n" + smp_file)

        # : : : : : : : : : : : : : : :
        # Zone Creation

        # create zones based on sound
        for idx, sound in enumerate(sounds):

            Zone.create(self, sound)

        # : : : : : : : : : : : : : : :
        # Post Processing

        # sort zones tonally
        self.sort_zones_by_note()

        # spread tonal range of zones
        if mapping_type == "tonal":
            self.spread_zones_tonal_range()
        else:
            # atonal gets a special treadment
            self.spread_zones_tonal_range_atonal(mapping_step)

        # crossfade zones
        self.crossfade_zones()

        # polymono implementation
        self.apply_polymono()

        # auto-adjust levels of zone (includes crossfades)
        self.adjust_all_zone_levels()

        # automatically index round robins
        self.setup_sequences()

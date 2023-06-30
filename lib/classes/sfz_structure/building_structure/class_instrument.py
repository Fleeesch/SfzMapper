# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sfz Structure : Instrument
#
#   Chain of Creation:
#   Builder > [Instrument] > Part > Zone > Split > Sound
#
#   Instrument that contains all the data for
#   a potential SFZ file.
#
#   Stores global lookup data for all the building
#   blocks contained in it.
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from datetime import date

from lib import lookup, message
from lib.classes.audio_processor.equalizer.class_equalizer import Equalizer
from lib.classes.audio_processor.filter.class_filter import Filter
from lib.classes.class_file import File
from lib.classes.control.class_control import Control
from lib.classes.modulation.release_envelope.class_release_envelope import \
    ReleaseEnvelope
from lib.classes.sfz_structure.helpers.range.elements.class_keyswitch import \
    KeySwitch
from lib.config import config

from ...class_writer import Writer
from ..class_sfz_structure import SfzStructure
from .class_part import Part

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Instrument(SfzStructure):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # list of all created instruments
    lookup = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Clear Lookup
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    @staticmethod
    def clear_lookup():
        # clear lookup list
        Instrument.lookup = []

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Create
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def create(builder, name):

        # create instance
        ins = Instrument(builder, name)

        # store into builder lookup
        builder.instruments[name] = ins

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, builder, name):

        # super constructor
        super().__init__(self)

        # indicator of a successful build
        self.build_success = False

        # store attributes
        self.builder = builder
        self.name = name

        # parts
        self.parts = {}

        # groups
        self.groups = []
        self.group_index = 1

        # curve lookup and index
        self.curves = {}
        self.curve_index = 8

        # envelope lookup and index
        self.envelopes = {}
        self.envelope_index = 0

        # LFO lookup and index
        self.lfo = {}
        self.lfo_index = 0

        # keyswitches
        self.keyswitches = {}
        self.keyswitches_min = 0
        self.keyswitches_max = 127

        # variables
        self.variables = {}
        self.variable_index = 0

        # store instrument part of data map
        self.map_data = self.builder.map_data["instruments"][self.name]

        # merge instrument part with defaults
        self.map_data = config.merge_with_defaults(self.map_data, "instruments")

        # hide flag
        self.hide = self.map_data["hide"]

        # declare and load controls
        self.controls = {}
        self.load_controls()

        # declare and load filters
        self.filters = {}
        self.load_filters()
        
        # declare and load equalizers
        self.equalizers = {}
        self.load_equalizers()

        # declare load release envelopes
        self.release_envelopes = {}
        self.load_release_envelopes()

        # create file
        self.file = File(self.builder.map_path, self.generate_sfz_name())

        # go through listed parts in data pool
        for part in self.map_data["parts"]:
            
            # try creating a part
            try:
                # create part and add to instrument lookup dictionary
                self.parts[part] = Part.create(self, part, self.map_data["parts"][part])

                # success message
                message.progress("+ Part " + part)

                # mark build as done
                self.build_successful()
                message.success()
            except:
                # generic error message
                message.error("Something went wrong when creating the Part")

        # load attributes
        self.load_attributes(self.map_data)

        # load settings
        self.load_settings(self.map_data)

        # add innstrument to global lookup
        Instrument.lookup.append(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Equalizers
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_equalizers(self):

        # merge equalizer data with defaults
        self.map_data["equalizers"] = config.merge_with_defaults(self.map_data["equalizers"], "equalizers")

        # go through filters
        for eq in self.map_data["equalizers"]:

            eq_data = self.map_data["equalizers"][eq]

            # merge filter section with defaults
            eq_data = config.merge_with_defaults(eq_data, "equalizer element")

            # dynamic setting
            dynamic = eq_data["dynamic"]

            # get band data
            band_data = eq_data["bands"]

            # skip eq if there are no bands
            if band_data is None:
                continue

            # create eq
            eq_new = Equalizer(self)

            # eq dynamic setting
            eq_new.dynamic = dynamic

            # go through bands, add them one by one
            for band in band_data:
                b = eq_new.add_band(band[0], band[1], band[2])

            # store equalizer in instrument lookup
            self.equalizers[eq] = eq_new

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Filters
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_filters(self):

        # merge filter data with defaults
        self.map_data["filters"] = config.merge_with_defaults(self.map_data["filters"], "filters")

        # go through filters
        for filter in self.map_data["filters"]:

            # get filter data address
            fil_data = self.map_data["filters"][filter]

            # merge filter section with defaults
            fil_data = config.merge_with_defaults(fil_data, "filter element")

            # get attributes
            type = fil_data["type"]
            poles = fil_data["poles"]
            frequency = fil_data["frequency"]
            resonance = fil_data["resonance"]
            gain = fil_data["gain"]
            keytrack = fil_data["key tracking"]
            keycenter = fil_data["key tracking center"]
            veltrack = fil_data["velocity tracking"]

            # create filter instance
            fil_new = Filter(self)

            # set type and poles
            fil_new.set_type(type, poles)

            # set attributes
            fil_new.frequency.depth = frequency
            fil_new.resonance.depth = resonance
            fil_new.gain.depth = gain
            fil_new.keytrack = keytrack
            fil_new.keytrack_center = keycenter
            fil_new.velocity_track = veltrack

            # store filter in instrument lookup
            self.filters[filter] = fil_new

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Controls
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_controls(self):

        # merge control section with defaults
        self.map_data["control"] = config.merge_with_defaults(self.map_data["control"], "control")

        # go through controls
        for ctrl in self.map_data["control"]:

            # store address to control
            address = self.map_data["control"][ctrl]

            # merge control element with defaults
            address = config.merge_with_defaults(address, "control element")

            # skip flag
            skip = False

            # check if control exists
            for ctrl_comp in self.controls:
                if self.controls[ctrl_comp].cc == address["cc"]:
                    skip = True

            # skip creating a new control already exists
            if skip:
                continue

            # create control linked to this instrument
            Control(self, address["cc"], ctrl, address["default"], address["hide"], address["show cc"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Release Envelopes
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_release_envelopes(self):

        # merge control section with defaults
        self.map_data["release envelopes"] = config.merge_with_defaults(self.map_data["release envelopes"], "release envelopes")

        # go through controls
        for env in self.map_data["release envelopes"]:

            # store address to control
            address = self.map_data["release envelopes"][env]

            # merge control element with defaults
            address = config.merge_with_defaults(address, "release envelope element")

            # create release envelope
            env_new = ReleaseEnvelope(self)

            # store day value
            env_new.decay = address["decay"]

            # only add points if there is any data
            if address["points"] and type(address["points"]) is list:

                # go through points
                for point in address["points"]:

                    # store point attributes
                    level = point[0]
                    time = point[1]

                    # add point to envelope
                    env_new.add_point(time, level)

            # store created envelope in lookup
            self.release_envelopes[env] = env_new

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Generate File Name
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def generate_sfz_name(self, has_extension=True):

        if "$" in self.name:
            if has_extension:
                return self.builder.map_data["name"] + ".sfz"
            else:
                return self.builder.map_data["name"]

        if has_extension:
            return self.builder.map_data["name"] + " - " + self.name + ".sfz"
        else:
            return self.builder.map_data["name"] + " - " + self.name

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Build Successful
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def build_successful(self):
        self.build_success = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ LFO
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_lfo(self):

        data = ""

        for lfo in self.lfo:
            data += self.lfo[lfo].get_sfz() + "\n"

        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Envelopes
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_envelopes(self):

        data = ""

        for env in self.envelopes:
            data += self.envelopes[env].get_sfz() + "\n"

        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ controls
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_controls(self):

        # sfz string
        data = ""

        # go through controls
        for control in self.controls:

            # get sfz
            sfz = self.controls[control].get_sfz_code()

            # only add lines if content is available
            if sfz:
                # comment header
                data += "// " + self.controls[control].label + "\n"
                # data
                data += sfz

        # return sfz lines
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Write SFZ File
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def write_sfz_file(self):

        # don't write if build has failed
        if not self.build_success:
            return

        # include elements that will be included via inserts
        for part in self.parts:

            self.parts[part].get_sfz_insert(False)

            for zone in self.parts[part].zones:

                zone.get_sfz_insert(False)

                for split in zone.splits:

                    split.get_sfz_insert(False)

                    for sound in split.sounds:

                        split.get_sfz_insert(False)

        # setup initial writers
        wrt_start = Writer(self, self.file)
        wrt_control = Writer(self, self.file)
        wrt_curve = Writer(self, self.file)
        wrt_master = Writer(self, self.file)

        # collect instrument header information
        header_info = ""
        header_info += "    " + self.generate_sfz_name(False) + "\n"
        header_info += "$c" + "\n"
        header_info += "//        " + lookup.DATE_STRING + "\n"
        header_info += "//        " + lookup.SOFTWARE_IDENT_STRING + "\n"

        # write header info
        wrt_start.comment_large(header_info)

        # * * * * * * * * * * * * * *
        #   Curves

        # print curves if available
        if self.curves:
            wrt_curve.comment_block("Curves")
            for curve in self.curves:
                wrt_curve.text(self.curves[curve].get())

        # * * * * * * * * * * * * * *
        #   Control

        # Control Section
        wrt_control.comment_block("Control")
        wrt_control.header("control")
        wrt_control.text(self.get_sfz_controls())

        # * * * * * * * * * * * * * *
        #   Master

        # Print Master Header
        wrt_master.comment_block("Master")
        wrt_master.header("master")

        # Insert Text (Pre)
        wrt_master.text(self.get_sfz_insert()[0])

        # Keyswitch Range
        keyswitch_sfz = KeySwitch.get_sfz_global_range(self)

        if keyswitch_sfz:
            wrt_master.comment("Keyswitch Range")
            wrt_master.text(keyswitch_sfz)

        # Pitchbend
        if self.pitchbend:
            wrt_master.comment("Pitchbend")
            wrt_master.text(self.pitchbend.get_sfz())

        # Variables
        variables_sfz = self.get_sfz_variables()

        if variables_sfz:
            wrt_master.comment_line("Variables")
            wrt_master.text(variables_sfz)

        # LFOs
        lfo_sfz = self.get_sfz_lfo()

        if lfo_sfz:
            wrt_master.comment_line("LFOs")
            wrt_master.text(lfo_sfz)

        # Envelopes
        envelopes_sfz = self.get_sfz_envelopes()

        if envelopes_sfz:
            wrt_master.comment_line("Envelopes")
            wrt_master.text(envelopes_sfz)

        # Settings
        settings_sfz = self.get_sfz_settings()

        if settings_sfz:
            wrt_master.comment("Settings")
            wrt_master.text(settings_sfz)

        # Attributes
        attributes_sfz = self.get_sfz_attributes()

        if attributes_sfz:
            wrt_master.comment("Attributes")
            wrt_master.text(attributes_sfz)

        # Amplitude Envelope

        if self.ampeg:
            ampeg_sfz = self.ampeg.get_sfz()

            if ampeg_sfz:
                wrt_master.comment("Amplitude Envelope")
                wrt_master.text(self.ampeg.get_sfz())

        # Insert Text (Post)
        wrt_master.text(self.get_sfz_insert()[1])

        for part in self.parts:

            # * * * * * * * * * * * * * *
            #   Parts

            part_inst = self.parts[part]

            # ignore hidden parts or the ones that are without zones
            if part_inst.hide or not part_inst.zones:
                continue

            # create writer for section
            wrt_part = Writer(self, self.file)

            # Header of Group
            wrt_part.comment_block("Part : " + part_inst.name)
            wrt_part.header("group")

            # Insert Text (Pre)
            include_insert = part_inst.get_sfz_insert()[0]

            if include_insert:
                wrt_part.comment("Custom Insert")
                wrt_part.text(include_insert)

            # Include (Pre)
            include_sfz = part_inst.get_sfz_includes()[0]

            if include_sfz:
                wrt_part.comment("Include")
                wrt_part.text(include_sfz)

            # Keytrigger Bypass
            if part_inst.disable_keytrigger:
                wrt_part.comment("Keytrigger Bypass")
                wrt_part.text(part_inst.get_sfz_keytrigger_bypass())

            # Pedal Data
            if part_inst.pedals:
                wrt_part.comment("Pedals")
                wrt_part.text(part_inst.get_sfz_pedals())

            # CC Range
            if part_inst.range_cc:
                wrt_part.comment("CC Range")
                wrt_part.text(part_inst.get_sfz_cc_range())

            # CC Range Trigger
            if part_inst.range_cc_trigger:
                wrt_part.comment("CC Range Trigger")
                wrt_part.text(part_inst.get_sfz_cc_range_trigger())

            # Program Change
            if part_inst.range_program:
                wrt_part.comment("Program Range")
                wrt_part.text(part_inst.get_sfz_program_range())
            
            # Keyswitch
            if part_inst.keyswitch:
                keyswitch_sfz = part_inst.keyswitch.get_sfz()

                if keyswitch_sfz:
                    wrt_part.comment("Keyswitch")
                    wrt_part.text(keyswitch_sfz)

            # Pitchbend
            if part_inst.pitchbend:
                wrt_part.comment("Pitchbend")
                wrt_part.text(part_inst.pitchbend.get_sfz())

            # Settings
            settings_sfz = part_inst.get_sfz_settings()
            part_sfz = part_inst.get_sfz_part()
            
            if part_sfz or settings_sfz:
                wrt_part.comment("Settings")

            if part_sfz:
                wrt_part.text(part_sfz)

            if settings_sfz:
                wrt_part.text(settings_sfz)

            # Attributes
            attributes_sfz = part_inst.get_sfz_attributes()

            if attributes_sfz:
                wrt_part.comment("Attributes")
                wrt_part.text(attributes_sfz)

            # print filter lines
            filter_sfz = part_inst.get_sfz_local_filters()

            if filter_sfz:
                wrt_part.comment("Filters")
                wrt_part.text(filter_sfz)

            # print equalizer lines
            equalizer_sfz = part_inst.get_sfz_local_equalizer()

            if equalizer_sfz:
                wrt_part.comment("Equalizer")
                wrt_part.text(equalizer_sfz)

            # Amplitude Envelope
            if part_inst.ampeg:
                wrt_part.comment("Amp EG")
                wrt_part.text(part_inst.ampeg.get_sfz())

            # Release Envelope
            if part_inst.release_envelope:
                wrt_part.comment("Release Envelope")
                wrt_part.text(part_inst.release_envelope.get_sfz())

            # Include (Post)
            include_sfz = part_inst.get_sfz_includes()[1]

            if include_sfz:
                wrt_part.comment("Include")
                wrt_part.text(include_sfz)

            # Insert Text (Post)
            insert_sfz = part_inst.get_sfz_insert()[1]

            if insert_sfz:
                wrt_part.comment("Custom Insert")
                wrt_part.text(insert_sfz)
            
            # ::: Phantom Zone :::
            if part_inst.phantom_zone:
                wrt_part.comment_line("Phantom Zone")
                wrt_part.text(part_inst.phantom_zone.get_sfz())

            for zone in part_inst.zones:

                # * * * * * * * * * * * * * *
                #   Zones

                # create writer for section
                wrt_zone = Writer(self, self.file)

                # Note Range
                if not part_inst.disable_keytrigger:
                    wrt_zone.comment_line("Note Range : " + str(zone.note_low) + " - " + str(zone.note_high))
                else:
                    wrt_zone.comment_line("Region")

                # store note range
                note_low = zone.note_low
                note_high = zone.note_high

                # ::: Phantom Zone :::
                if zone.phantom_zone:
                    wrt_zone.comment_line("Phantom Zone")
                    wrt_zone.text(zone.phantom_zone.get_sfz())

                for split in zone.splits:

                    # * * * * * * * * * * * * * *
                    #   Splits

                    # create writer for section
                    wrt_split = Writer(self, self.file)

                    # level description
                    wrt_split.comment_sub("Level " + str(split.level_low) + " - " + str(split.level_high), 1)

                    # level range
                    level_low = split.level_low
                    level_high = split.level_high

                    # level crossfades
                    crossfade_low_start = split.crossfade_low_start
                    crossfade_low_end = split.crossfade_low_end
                    crossfade_high_start = split.crossfade_high_start
                    crossfade_high_end = split.crossfade_high_end

                    for sound in split.sounds:

                        # * * * * * * * * * * * * * *
                        #   Sound

                        # create writer for section
                        wrt_sound = Writer(self, self.file)

                        # Round Robin
                        if sound.sequence:
                            for idx, s in enumerate(sound.sequence.sounds):
                                if s == sound:
                                    wrt_sound.comment_sub("RoundRobin" + str(idx + 1), 2)
                                    break

                        # Header of Region
                        wrt_sound.header("region")

                        # Insert Text (Pre)
                        wrt_sound.text(sound.get_sfz_insert()[0])

                        # Sample Source
                        wrt_sound.comment("Sample Source")
                        wrt_sound.tag("sample", sound.get_sample_location())

                        # Reverse playback
                        wrt_sound.comment("Playback Direction")
                        if part_inst.reverse:
                            wrt_sound.tag("direction", "reverse")
                        else:
                            wrt_sound.tag("direction", "forward")

                        # Choke Group (Sound)
                        choke_sfz_sound = sound.get_sfz_group_data()

                        # Choke Group (Zone)
                        choke_sfz_zone = zone.get_sfz_group_data()

                        # Choke Group (Part)
                        choke_sfz_part = part_inst.get_sfz_group_data()
                        
                        # Choke Group Settings
                        
                        if choke_sfz_sound:
                            wrt_sound.comment("Choke Group")
                            wrt_sound.text(sound.get_sfz_group_data())

                        elif choke_sfz_zone:
                            wrt_sound.comment("Choke Group")
                            wrt_sound.text(zone.get_sfz_group_data())
                            wrt_sound.text(part_inst.get_sfz_group_data(True))

                        elif choke_sfz_part:
                            wrt_sound.comment("Choke Group")
                            wrt_sound.text(part_inst.get_sfz_group_data())

                        # Attributes
                        attributes_sfz = sound.get_sfz_attributes()

                        if attributes_sfz:
                            wrt_sound.comment("Attributes")
                            wrt_sound.text(attributes_sfz)

                        # Settings
                        settings_sfz = sound.get_sfz_settings()

                        crossfade_curve_sfz = ""

                        if split.crossfade:
                            crossfade_curve_sfz = split.crossfade.get_sfz()

                        if settings_sfz or crossfade_curve_sfz:
                            wrt_sound.comment("Settings")

                        if crossfade_curve_sfz:
                            wrt_sound.text(crossfade_curve_sfz)

                        if settings_sfz:
                            wrt_sound.text(settings_sfz)

                        # Note Range
                        if not part_inst.disable_keytrigger:

                            wrt_sound.comment("Note Range")

                            wrt_sound.tag("pitch_keycenter", sound.keycenter)

                            if note_low != note_high:
                                wrt_sound.tag("lokey", note_low)
                                wrt_sound.tag("hikey", note_high)

                            else:
                                wrt_sound.tag("key", note_low)

                            if zone.use_crossfades_low or zone.use_crossfades_high:
                                wrt_sound.comment("Note Crossfade")

                            # Note Crossfades Low
                            if zone.use_crossfades_low:
                                wrt_sound.tag("xfin_lokey", zone.crossfade_low_start)
                                wrt_sound.tag("xfin_hikey", zone.crossfade_low_end)

                            # Note Crossfades High
                            if zone.use_crossfades_high:
                                wrt_sound.tag("xfout_lokey", zone.crossfade_high_start)
                                wrt_sound.tag("xfout_hikey", zone.crossfade_high_end)

                            # Note Center
                            if sound.keytrack != 0:
                                if sound.keycenter:
                                    wrt_sound.tag("pitch_keycenter", sound.keycenter)
                                elif zone.note_center != zone.note:
                                    wrt_sound.tag("pitch_keycenter", zone.note_center)

                        # Level Range
                        if not split.force_full_range:
                            wrt_sound.comment("Level Range")
                            wrt_sound.tag(split.get_sfz_range("lo"), level_low)
                            wrt_sound.tag(split.get_sfz_range("hi"), level_high)

                        # Fade In
                        if crossfade_low_start != crossfade_low_end or crossfade_high_start != crossfade_high_end:
                            wrt_sound.comment("Level Crossfade")

                        if crossfade_low_start != crossfade_low_end:
                            wrt_sound.tag(split.get_sfz_range("xfin_lo"), crossfade_low_start)
                            wrt_sound.tag(split.get_sfz_range("xfin_hi"), crossfade_low_end)

                        # Fade Out
                        if crossfade_high_start != crossfade_high_end:
                            wrt_sound.tag(split.get_sfz_range("xfout_lo"), crossfade_high_start)
                            wrt_sound.tag(split.get_sfz_range("xfout_hi"), crossfade_high_end)

                        # Sequence Trigger
                        if sound.sequence:
                            wrt_sound.comment("Possibility")

                            # Random
                            if sound.use_random:
                                wrt_sound.tag("lorand", str(sound.random_low))
                                wrt_sound.tag("hirand", str(sound.random_high))

                            # Sequence
                            if sound.use_sequence:
                                wrt_sound.tag("seq_length", str(sound.sequence_length))
                                wrt_sound.tag("seq_position", str(sound.sequence_position))

                        # Insert Text (Post)
                        wrt_sound.text(sound.get_sfz_insert()[1])

        # print writer content to file unless not allowed to
        if not self.hide:
            self.file.write_all()

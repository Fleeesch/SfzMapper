# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : SFZ Structure
#
#   The most basic building block of a SFZ
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


from lib import lookup
from lib.classes.audio_processor.ampeg.class_ampeg import AmpEg
from lib.classes.audio_processor.equalizer.class_equalizer import Equalizer
from lib.classes.audio_processor.filter.class_filter import Filter
from lib.classes.sfz_structure.attributes.class_attribute import Attribute
from lib.classes.sfz_structure.control.pedal.elements.class_pedal_sostenuto import PedalSostenuto
from lib.classes.sfz_structure.control.pedal.elements.class_pedal_sustain import PedalSustain
from lib.classes.sfz_structure.helpers.bend.class_pitchbend import Pitchbend
from lib.classes.sfz_structure.helpers.include.class_include import Include
from lib.classes.sfz_structure.settings.class_setting import Setting
from lib.config import config
from lib.config.reformat import reformat_ampeg as ref_amp

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SfzStructure:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Dynamic Dependencies
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument):

        # instrument (highest level of structure)
        self.instrument = instrument
        
        # hide flag (don't print to SFZ)
        self.hide = False
        
        # attributes
        self.attributes = []

        # attribute data pool
        self.attribute_pool = {}

        # settings
        self.settings = []

        # settings pool
        self.setting_pool = {}

        # group settings
        self.group = None
        self.group_polymono = None
        self.group_off = None
        self.group_time = None
        self.group_mode = None
        self.group_shape = None
        self.group_settings = []

        # pedals
        self.pedals = []

        # filters
        self.filters = []

        # equalizer
        self.equalizer = None

        # keyswitch
        self.keyswitch = None

        # phantom zone
        self.phantom_zone = None

        # release envelope
        self.release_envelope = None

        # keytrigger bypass
        self.disable_keytrigger = False

        # Amplitude EG
        self.ampeg = None

        # CC Range
        self.range_cc = []

        # CC Range Trigger
        self.range_cc_trigger = []

        # Program Change Range
        self.range_program = None

        # Include
        self.include = None

        # Pitchbend
        self.pitchbend = None

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Include
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_includes(self):

        # load include list
        include_list = self.map_data["include"]

        # skip if there is absolute
        if include_list is None:
            return

        # reformat include if not a dict
        if type(include_list) is not dict:

            # store single value
            inc = include_list

            # declare include list as dict
            include_list = {}
            # place value in post section by default
            include_list["post"] = inc

        # merge include with default structure
        include_list = config.merge_with_defaults(include_list, "include")

        # get working directory
        working_dir = self.instrument.builder.map_path

        # include instance
        inc_new = Include()

        # go through pre and post sections
        for pp in include_list:

            # convert include to list of isn't one already
            if type(include_list[pp]) is not list:
                include_list[pp] = [include_list[pp]]

            # go through includes
            for inc in include_list[pp]:

                # try loading data
                try:

                    # generate path
                    path = working_dir + "/" + str(inc)

                    # open file
                    file = open(path, "r")

                    # read data
                    data = file.read()

                    # append data to includes
                    if pp == "pre":
                        # pre
                        inc_new.add_content_pre(data)
                    if pp == "post":
                        # post
                        inc_new.add_content_post(data)
                except:
                    pass

        # store include instance
        self.include = inc_new

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Include
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_sfz_includes(self):

        # return nothing if there is no include
        if self.include is None:
            return ["", ""]

        # return include sfz
        return [self.include.get_sfz_pre(), self.include.get_sfz_post()]

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Inserts
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_insert(self, apply_wildcards=True):

        # init return array
        data = ["", ""]

        # try loading data directly
        try:
            # if insert data is a one liner, put it in the pre section
            if type(self.map_data["insert"]) is str:
                data[0] += self.apply_insert_wildcards(self.map_data["insert"], not apply_wildcards) + "\n"
            else:

                # alterantively try loading pre and post separately
                try:
                    data[0] += self.apply_insert_wildcards(self.map_data["insert"]["pre"], not apply_wildcards) + "\n"
                except:
                    pass

                try:
                    data[1] += self.apply_insert_wildcards(self.map_data["insert"]["post"], not apply_wildcards) + "\n"
                except:
                    pass

        except:
            pass

        # return data
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Group data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_group_data(self, ignore_numbers=False):

        data = ""

        # optionally return only non-group-number-data
        if ignore_numbers:

            # off mode
            if self.group_mode:
                data += "off_mode=" + str(self.group_mode) + "\n"

            # time
            if self.group_time:
                data += "off_time=" + str(self.group_time) + "\n"

            # shape
            if self.group_shape:
                data += "off_shape=" + str(self.group_shape) + "\n"

            return data

        # group number
        if self.group:
            data += "group=" + str(self.group.get_index()) + "\n"

        # off-group data
        if self.group_off:

            # off-group number
            data += "off_by=" + str(self.group_off.get_index()) + "\n"
            
            # off mode
            if self.group_mode:
                data += "off_mode=" + str(self.group_mode) + "\n"

            # time
            if self.group_time:
                data += "off_time=" + str(self.group_time) + "\n"

            # shape
            if self.group_shape:
                data += "off_shape=" + str(self.group_shape) + "\n"

        # return data
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Keyrange Bypass
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_keyrange_bypass(self):

        try:
            self.disable_keytrigger = self.map_data["keyrange"]["disable"]
        except:
            return

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Pedal Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_pedal_settings(self):
        
        # try loading pedal section
        try:

            # load data
            pedal_data = self.map_data["pedals"]

            # skip if there's no pedal data
            if not pedal_data:
                return

            # merge data with default values
            pedal_data = config.merge_with_defaults(pedal_data, "pedals")

            # go through pedal types
            for pedal in ["sustain", "sostenuto"]:

                # try loading data
                try:

                    # store data entries
                    bypass = pedal_data[pedal]["bypass"]
                    cc = pedal_data[pedal]["cc"]
                    off_val = pedal_data[pedal]["off value"]

                    # bypass enabled?
                    if bypass:

                        # create bypassed pedal through invalid cc number
                        if pedal == "sustain":
                            self.pedals.append(PedalSustain(-1, 0))
                        if pedal == "sostenuto":
                            self.pedals.append(PedalSostenuto(-1, 0))

                    # pedal enabled?
                    else:

                        # make sure valid values are available
                        if cc or off_val:

                            # create pedal based on type
                            if pedal == "sustain":
                                self.pedals.append(PedalSustain(cc, off_val))
                            if pedal == "sostenuto":
                                self.pedals.append(PedalSostenuto(cc, off_val))

                except:
                    # skip paedal on error
                    continue

        except:
            return

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Pitchbend Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def load_pitchbend_settings(self):

        try:

            # load pitchbend data
            pb = self.map_data["pitchbend"]

            # merge with pitchbend defaults
            pb = config.merge_with_defaults(pb, "pitchbend")

            # declare settings
            smoothing = 0
            range = 0
            step = 0

            # load smoothing
            smoothing = pb["smooth"]
            
            # load range (either from a list or as a single value)
            if type(pb["range"]) is list:
                range = [0, 0]
                range[0] = pb["range"][0]
                range[1] = pb["range"][1]
            else:
                range = pb["range"]

            # load step (either from a list or as a single value)
            if type(pb["step"]) is list:
                step = [0, 0]
                step[0] = pb["step"][0]
                step[1] = pb["step"][1]
            else:
                step = pb["step"]

            # create pitchbend instance
            pb_new = Pitchbend(self, range, step, smoothing)

            # refer to pitchbend instance in structure
            self.pitchbend = pb_new

        except:
            pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Group Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def load_group_settings(self):
        
        
        from lib.classes.sfz_structure.group.class_group import Group
        
        # create choke data placeholder if it doesn't exist
        try:
            self.map_data["choke"]
        except:
            self.map_data["choke"] = {}
            return
        
        # merge group data with defaults
        self.map_data["choke"] = config.merge_with_defaults(self.map_data["choke"], "choke")
        
        # load group data address
        group_data = self.map_data["choke"]
        
        # skip if there's no group data
        if not group_data:
            return
        
        # polymono data
        if group_data["polymono"]:
            self.group_polymono = True
        
        # only load group data of polymono is not active
        if not self.group_polymono:
            
            # group auto-increment
            if group_data["auto increment"]:    
               group_data["group"] = None 
                
            # group belonging
            if group_data["group"]:
                self.group = Group.add_group_to_instrument(self, group_data["group"], False)
            
            # off by group
            if group_data["off by"]:
                self.group_off = Group.add_group_to_instrument(self, group_data["off by"])
            
            # add generic group if necessary
            if self.group is None and self.group_off:
                self.group = Group.add_group_to_instrument(self, "Generic Group " + str(id(self)))
        
        # use release curve as off-time
        if group_data["hard off"]:
            self.group_mode = "fast"
        
        # use given time for off-time
        elif group_data["time"]:
            self.group_time = group_data["time"]
            self.group_mode = "time"
        
        # use default fast mode for off
        else:
            self.group_mode = "normal"

        # shape
        if group_data["shape"]:
            self.group_shape = group_data["shape"]

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Pedal SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_pedals(self):

        # sfz string
        data = ""

        # go through pedals
        for pedal in self.pedals:

            # add sfz data
            data += pedal.get_sfz() + "\n"

        # return sfz string
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get local Filter SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_local_filters(self):

        # sfz string
        data = ""

        # go through filters, collect sfz lines
        for filter in self.filters:
            data += filter.get_sfz()

        # return sfz string
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get local Equalizer SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_local_equalizer(self):

        # sfz string
        data = ""

        # add equalizer sfz if available
        if self.equalizer:
            data += self.equalizer.get_sfz()

        # return sfz string
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load local Equalizers
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_local_equalizer(self):

        # don't do anything if there is no data
        if self.map_data["equalizer"] is None:
            return

        # store data address
        eq_data = self.map_data["equalizer"]

        # get equalizer name
        for eq in eq_data:
            equalizer = eq

        # merge data with defaults
        eq_data[eq] = config.merge_with_defaults(eq_data[eq], "part equalizer element")

        # copy equalizer from instrument pool
        eq_new = Equalizer.copy_equalizer(self, equalizer)

        # skip if there's no filter available
        if eq_new is None:
            return

        # load equalizer modulation
        eq_new.load_modulation(eq_data[eq]["modulation"])

        # store equalizer in structure lookup
        self.equalizer = eq_new

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load local Filters
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_local_filters(self):

        # don't do anything if there is no data
        if self.map_data["filters"] is None:
            return

        # go through filter list
        for idx, filter in enumerate(list(self.map_data["filters"])):

            # respect 2 filter limit
            if idx >= 2:
                break

            # store data address
            fil_data = self.map_data["filters"][filter]

            # merge data with defaults
            fil_data = config.merge_with_defaults(fil_data, "part filter element")

            # copy filter from instrument pool
            fil_new = Filter.copy_filter(self, filter)

            # skip if there's no filter available
            if fil_new is None:
                continue

            # load modulation
            fil_new.load_modulation(fil_data["modulation"])

            # add filter to lookup list
            self.filters.append(fil_new)

            # store filter index number
            fil_new.index = len(self.filters)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Amp EG
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_amp_eg(self):

        try:
            ampeg_data = self.map_data["amp eg"]
            ampeg_data = ref_amp.reformat_ampeg(ampeg_data)
            ampeg_data = config.merge_with_defaults(self.map_data["amp eg"], "amp eg")

            AmpEg(self, ampeg_data)

        except:
            pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Release Envelope
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_release_envelope(self):

        try:
            env = self.map_data["release envelope"]

            for env_comp in self.instrument.release_envelopes:
                if env_comp == env:
                    self.release_envelope = self.instrument.release_envelopes[env_comp]

        except:
            pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ CC Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_cc_range(self):

        # return string
        data = ""

        # collection sfz lines from ranges
        for rng in self.range_cc:
            data += rng.get_sfz()

        # return sfz data
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ CC Range Trigger
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_cc_range_trigger(self):

        # return string
        data = ""

        # collection sfz lines from ranges
        for rng in self.range_cc_trigger:
            data += rng.get_sfz()

        # return sfz data
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ Program Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_program_range(self):

        # get sfz lines from program range
        return self.range_program.get_sfz()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load CC Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_cc_range(self):

        lookup.add_cc_range_via_lookup(self)
        lookup.add_cchd_range_via_lookup(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load CC Range Trigger
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_cc_range_trigger(self):

        lookup.add_cc_range_trigger_via_lookup(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Program Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_program_range(self):

        lookup.add_program_range_via_lookup(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Keyswitch
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_keyswitch(self):

        self.keyswitch = lookup.add_keyswitch_via_lookup(self.instrument, self, self.map_data["keyswitch"])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Keytrigger Bypass
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_keytrigger_bypass(self):

        data = ""
        
        # force invalid cc range
        data += "lokey=-1" + "\n"
        data += "hikey=-1" + "\n"

        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Settings SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_settings(self):

        data = ""

        for set in self.settings:

            # append settings line
            data += set.get_sfz() + "\n"

        # return the line array
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Attributes SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_attributes(self):

        data = ""

        # go through attributes
        for att in self.attributes:

            # get lines of attribute
            att_data = att.get_sfz_lines()

            # append lines to return string array
            for line in att_data:
                data += line + "\n"

        # return line array
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Variables SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_variables(self):

        data = ""

        # go through variables and collect modulation
        for var in self.variables:

            # get instance of variable
            var_inst = self.variables[var]

            var_lines = var_inst.get_modulation()

            for line in var_lines:
                data += line + "\n"

        # return the sfz string
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Envelopes SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_envelopes(self):

        lines = []

        # go through variables and collect modulation
        for env in self.envelopes:

            # get instance of variable
            env_inst = self.envelopes[env]

            env_lines = env_inst.get_modulation()

            for line in env_lines:
                lines.append(line)

        # return the line array
        return lines

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get LFO SFZ Lines
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_lfo(self):

        lines = []

        # go through variables and collect modulation
        for lfo in self.lfo:

            # get instance of variable
            lfo_inst = self.lfo[lfo]

            lfo_lines = lfo_inst.get_modulation()

            for line in lfo_lines:
                lines.append(line)

        # return the line array
        return lines

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def load_settings(self, data):

        # has to be a dict
        if type(data) is not dict:
            return

        # store settings pool
        self.setting_pool = data

        self.setup_loaded_settings()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Setup loaded Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def setup_loaded_settings(self):

        if not self.setting_pool:
            return

        for set in lookup.SETTING_LOOKUP:
            for tag in self.setting_pool:
                if tag == set:

                    set_new = Setting.add_from_tag(self.instrument, tag, self.setting_pool[tag])

                    self.settings.append(set_new)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Attributes
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_attributes(self, data):

        # has to be a dict
        if type(data) is not dict:
            return

        # store attribute pool
        self.attribute_pool = data

        # load attributes from pool
        self.setup_loaded_attributes()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Setup loaded Attributes
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def setup_loaded_attributes(self):

        # don't process an empty attribute pool
        if not self.attribute_pool:
            return

        for att in lookup.ATTRIBUTE_LOOKUP:
            for ent in self.attribute_pool:
                if ent == att:
                    self.setup_attribute(ent, self.attribute_pool[att])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Setup Attribute
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def setup_attribute(self, tag, data):

        # avoid all bools
        if type(data) is bool:
            return

        # setup default structure if data is a single value
        if not type(data) is dict:
            data = {"level": data}

        # merge data with default attributes
        data = config.merge_with_defaults(data, "attributes")

        from lib.config.reformat import \
            reformat_modulation_attribute as reformat

        # reformat modulation data
        data_mod = data["modulation"]
        data_mod = reformat.reformat_modulation_attribute(data_mod)

        # assume there is no attribute by default
        attr = None

        # ---------------------------
        #   Attribute List

        attr = Attribute.add_from_tag(self.instrument, data, tag)

        # ---------------------------
        #   Attribute Creation

        # add attribute to lookup list if valid
        if attr:

            attr.add_modulation(data_mod)

            self.attributes.append(attr)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Apply Insert Wildcards
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def apply_insert_wildcards(self, data, keep_data=False):

        import re

        # : : : : : : : : : : : : : : : : : : : :
        #   Sub-Method : Replace Tag
        # : : : : : : : : : : : : : : : : : : : :

        def replace_tag(data, old, new):

            if keep_data:
                return data

            return data.replace("{" + old + "}", str(new))

        # regex pattern for brackets
        pattern = r'\{([^}]*)\}'

        # collect all words matching pattern
        tags = re.findall(pattern, data)

        # go through collected tags
        for tag in tags:

            # try getting data
            try:

                # filter category and name
                category, name = tag.split(":")

                # ::: Envelopes

                if category == "envelopes":

                    # create envelope, replace tag with envelope tag
                    env = lookup.add_envelope_via_lookup(self.instrument, name)
                    data = replace_tag(data, tag, env.tag)

                # ::: Curves

                elif category == "curves":

                    # create curve, replace tag with curve index
                    crv = lookup.add_curve_via_lookup(self.instrument, name)
                    data = replace_tag(data, tag, crv.index)

                # ::: Filters

                if category == "filters":

                    # go through instrument filters
                    for fil_ins in self.instrument.filters:

                        # filter matches tag name? store filter
                        if fil_ins == name:
                            original_filter = self.instrument.filters[name]
                            break

                    # go through filters
                    for idx, filter in enumerate(self.filters):

                        # pick original filter that matches name
                        if filter.original_filter == original_filter:

                            # return SFZ-1 filter index number
                            if idx <= 0:
                                data = replace_tag(data, tag, "")
                            else:
                                data = replace_tag(data, tag, "2")

                # ::: LFO

                elif category == "lfo":

                    # create lfo, get tag
                    lfo = lookup.add_lfo_via_lookup(self.instrument, name)
                    data = replace_tag(data, tag, lfo.tag)

                # ::: Control

                elif category == "control":

                    # look for control, return cc number
                    ctrl = self.instrument.controls[name]
                    data = replace_tag(data, tag, ctrl.cc)

                # ::: Keyswitches

                elif category == "keyswitches":

                    # look for keyswitch, return low range number
                    ksw = lookup.add_keyswitch_via_lookup(self.instrument, self, name)
                    data = replace_tag(data, tag, ksw.get_range()[0])

                # ::: Keyswitches

                elif category == "keyswitches_high":

                    # look for keyswitch, return high range number
                    ksw = lookup.add_keyswitch_via_lookup(self.instrument, self, name)
                    data = replace_tag(data, tag, ksw.get_range()[1])

            except:
                # move on to next tag on error
                continue

        # return updated string
        return data

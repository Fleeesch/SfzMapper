# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Lookup
#
#   Global Data lookup, used for aliases and
#   to avoid circular imports
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# [!]
# You really should clean this up. No way this can't be done with a cleaner approach.

from datetime import date

from lib import version
from lib.classes.audio_processor.filter.type.class_filter_type_allpass import \
    FilterTypeAllpass
from lib.classes.audio_processor.filter.type.class_filter_type_bandpass import \
    FilterTypeBandpass
from lib.classes.audio_processor.filter.type.class_filter_type_comb import \
    FilterTypeComb
from lib.classes.audio_processor.filter.type.class_filter_type_eq import \
    FilterTypeEQ
from lib.classes.audio_processor.filter.type.class_filter_type_highpass import \
    FilterTypeHighpass
from lib.classes.audio_processor.filter.type.class_filter_type_highshelf import \
    FilterTypeHighShelf
from lib.classes.audio_processor.filter.type.class_filter_type_lowpass import \
    FilterTypeLowpass
from lib.classes.audio_processor.filter.type.class_filter_type_lowshelf import \
    FilterTypeLowShelf
from lib.classes.audio_processor.filter.type.class_filter_type_notch import \
    FilterTypeNotch
from lib.classes.audio_processor.filter.type.class_filter_type_pink import \
    FilterTypePink
from lib.classes.sfz_structure.attributes.tags.class_attribute_amplitude import \
    AttributeAmplitude
from lib.classes.sfz_structure.attributes.tags.class_attribute_delay import \
    AttributeDelay
from lib.classes.sfz_structure.attributes.tags.class_attribute_offset import \
    AttributeOffset
from lib.classes.sfz_structure.attributes.tags.class_attribute_pan import \
    AttributePan
from lib.classes.sfz_structure.attributes.tags.class_attribute_pitch import \
    AttributePitch
from lib.classes.sfz_structure.attributes.tags.class_attribute_tune import \
    AttributeTune
from lib.classes.sfz_structure.attributes.tags.class_attribute_volume import \
    AttributeVolume
from lib.classes.sfz_structure.attributes.tags.class_attribute_width import \
    AttributeWidth
from lib.classes.sfz_structure.settings.tags.class_setting_lastnote import \
    SettingLastNote
from lib.classes.sfz_structure.settings.tags.class_setting_note_offset import \
    SettingNoteOffset
from lib.classes.sfz_structure.settings.tags.class_setting_octave_offset import \
    SettingOctaveOffset
from lib.classes.sfz_structure.settings.tags.class_setting_pan_keytrack import \
    SettingPanKeytrack
from lib.classes.sfz_structure.settings.tags.class_setting_pan_law import \
    SettingPanLaw
from lib.classes.sfz_structure.settings.tags.class_setting_pan_random import \
    SettingPanRandom
from lib.classes.sfz_structure.settings.tags.class_setting_phase import \
    SettingPhase
from lib.classes.sfz_structure.settings.tags.class_setting_pitch_keytrack import \
    SettingPitchKeytrack
from lib.classes.sfz_structure.settings.tags.class_setting_playmode import \
    SettingPlaymode
from lib.classes.sfz_structure.settings.tags.class_setting_polyphony import \
    SettingPolyphony
from lib.classes.sfz_structure.settings.tags.class_setting_selfmask import \
    SettingSelfMask
from lib.classes.sfz_structure.settings.tags.class_setting_transpose import \
    SettingTranspose
from lib.classes.sfz_structure.settings.tags.class_setting_trigger import \
    SettingTrigger
from lib.classes.sfz_structure.settings.tags.class_setting_velocity_tracking import \
    SettingVelocityTracking
from lib.classes.sfz_structure.settings.tags.class_setting_voicecount import \
    SettingVoiceCount
from lib.interfaces.compensation.class_modulatable_compensation_average import \
    ModulatableCompensationAverage
from lib.interfaces.compensation.class_modulatable_compensation_sum import \
    ModulatableCompensationSum
from lib.interfaces.type.class_modulatable_modtyp_add import ModulationTypeAdd
from lib.interfaces.type.class_modulatable_modtyp_multiply import \
    ModulationTypeMultiply

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Lookup Strings
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DATE_STRING = ""

SOFTWARE_IDENT_STRING = "Created using SFZ Mapper " + version.get_version_string()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Generate Date String
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def generate_data_string():
    
    global DATE_STRING

    DATE_STRING = "Date: " + date.today().strftime("%b-%d-%Y")


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   ARIA Exclusive Attributes
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# ARIA exclusive CC numbers
CC_ARIA_PITCHBEND = 128
CC_CHANNEL_AT = 129
CC_POLY_AT = 130
CC_ARIA_VEL_ON = 131
CC_ARIA_VEL_OFF = 132
CC_ARIA_NOTE_NR = 133
CC_ARIA_NOTE_GATE = 134
CC_ARIA_RAND_UNI = 135
CC_ARIA_RAND_BI = 136
CC_ARIA_ALTERNATE = 137

# ARIA Sub-LFO limit
ARIA_LFO_SUB_LIMIT = 8

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Generator : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

GENERATOR = {

    "sine": "*sine",
    "saw": "*saw",
    "square": "*square",
    "tri": "*tri",
    "triangle": "*triangle",
    "noise": "*noise",
    "silence": "*silence",
    "": "*silence"

}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   LFO Waveform : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

LFO_WAVEFORM = {

    "triangle": 0,
    "sine": 1,
    "pulse 75": 2,
    "pulse 50": 3,
    "square": 3,
    "pulse": 3,
    "pulse 25": 4,
    "pulse 12.5": 5,
    "saw up": 6,
    "saw": 7,
    "saw down": 7,
    "sample and hold": 12,
    "sample": 12,
    "sample & hold": 12

}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Compensation Type : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

COMPENSATION_TYPE = {

    "sum": ModulatableCompensationSum,
    "average": ModulatableCompensationAverage,

}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Modulation Type : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

MODTYPE_LOOKUP = {

    "add": ModulationTypeAdd,
    "multiply": ModulationTypeMultiply

}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Filter : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


# link YAML tags to Filter Type Classes
FILTER_LOOKUP = {
    "lowpass": FilterTypeLowpass,
    "highpass": FilterTypeHighpass,
    "bandpass": FilterTypeBandpass,
    "notch": FilterTypeNotch,
    "allpass": FilterTypeAllpass,
    "comb": FilterTypeComb,
    "pink": FilterTypePink,
    "low-shelf": FilterTypeLowShelf,
    "high-shelf": FilterTypeHighShelf,
    "eq": FilterTypeEQ

}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Setting : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# link YAML tags to Setting Classes
SETTING_LOOKUP = {
    "trigger": SettingTrigger,
    "playmode": SettingPlaymode,
    "pitch tracking": SettingPitchKeytrack,
    "velocity tracking": SettingVelocityTracking,
    "midi transpose": SettingNoteOffset,
    "midi octave transpose": SettingOctaveOffset,
    "pan law": SettingPanLaw,
    "pan random": SettingPanRandom,
    "pan keytrack": SettingPanKeytrack,
    "phase": SettingPhase,
    "transpose": SettingTranspose,
    "last note": SettingLastNote,
    "selfmask": SettingSelfMask,
    "polyphony": SettingPolyphony,
    "voice count": SettingVoiceCount
}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Attribute : Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# link YAML tags  to Attribute Classes
ATTRIBUTE_LOOKUP = {
    "volume": AttributeVolume,
    "amp": AttributeAmplitude,
    "trim": AttributeAmplitude,
    "sample offset": AttributeOffset,
    "pan": AttributePan,
    "width": AttributeWidth,
    "tune": AttributeTune,
    "pitch": AttributePitch,
    "delay": AttributeDelay
}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add CC Range via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def add_cc_range_via_lookup(structure):

    import lib.classes.sfz_structure.helpers.range.elements.class_range_cc as ref_cc
    import lib.config.config as config

    try:

        # get range data
        range = structure.map_data["cc range"]

        # skip empty range
        if range is None:
            return None

        # go through range controls
        for rng in range:

            try:

                # merge range data with defaults
                range[rng] = config.merge_with_defaults(range[rng], "range element")

                # get control cc number
                cc = structure.instrument.controls[rng]

                # create range instance
                range_new = ref_cc.RangeCC(structure, cc)

                # set range
                range_new.set_range(range[rng]["low"], range[rng]["high"])

            except:
                pass

    except:
        pass

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add HD CC Range via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def add_cchd_range_via_lookup(structure):

    import lib.classes.sfz_structure.helpers.range.elements.class_range_cc_hd as ref_cc
    import lib.config.config as config

    try:

        # get range data
        range = structure.map_data["cchd range"]

        # skip empty range
        if range is None:
            return None

        # go through range controls
        for rng in range:

            try:

                # merge range data with defaults
                range[rng] = config.merge_with_defaults(range[rng], "range element")

                # get control cc number
                cc = structure.instrument.controls[rng]

                # create range instance
                range_new = ref_cc.RangeCCHD(structure, cc)

                # set range
                range_new.set_range(range[rng]["low"], range[rng]["high"])

            except:
                pass

    except:
        pass

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add CC Range Trigger via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def add_cc_range_trigger_via_lookup(structure):

    import lib.classes.sfz_structure.helpers.range.elements.class_range_cc_trigger as ref_cc
    import lib.config.config as config

    try:

        # get range data
        range = structure.map_data["cc trigger"]

        # skip empty range
        if range is None:
            return None

        # go through range controls
        for rng in range:

            try:

                # merge range data with defaults
                range[rng] = config.merge_with_defaults(range[rng], "range element")

                # get control cc number
                cc = structure.instrument.controls[rng]

                # create range instance
                range_new = ref_cc.RangeCCTrigger(structure, cc)

                # set range
                range_new.set_range(range[rng]["low"], range[rng]["high"])

            except:
                pass

    except:
        pass


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add Program Range via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def add_program_range_via_lookup(structure):

    import lib.classes.sfz_structure.helpers.range.elements.class_range_program as ref_rng
    import lib.config.config as config

    try:

        # get range data
        range = structure.map_data["program range"]

        # skip empty range
        if range is None:
            return None

        # merge range data with defaults
        range = config.merge_with_defaults(range, "range element")

        # create range instance
        range_new = ref_rng.RangeProgram(structure)

        # set range
        range_new.set_range(range["low"], range["high"])

    except:
        pass


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add keyswitch via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def add_keyswitch_via_lookup(instrument, structure, name):

    import lib.classes.sfz_structure.helpers.range.elements.class_keyswitch as ref_ks
    import lib.config.config as config

    # skip if there's no name
    if not name:
        return

    # load data
    data = structure.map_data

    # return existing keyswitch with identical name
    for ks in instrument.keyswitches:
        if ks == name:
            return instrument.keyswitches[ks]

    try:

        # get keyswitch data
        ks = instrument.map_data["keyswitches"][name]

        # merge keyswitch data with defaults
        ks = config.merge_with_defaults(ks, "keyswitch element")

        if ks["note"] is None:
            return None

        # create keyswitch instance
        ks_new = ref_ks.KeySwitch(structure, name)

        # set keyrange
        if ks["note"] is not None:
            if type(ks["note"]) is list:
                ks_new.set_range(ks["note"][0], ks["note"][1])
            else:
                ks_new.set_range(ks["note"], ks["note"])

        # return the created keyswitch
        return ks_new

    except:
        return None


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add Envlope via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def add_envelope_via_lookup(instrument, name):

    import lib.classes.modulation.envelope.class_envelope as ref_env
    import lib.config.config as config

    # load data
    data = instrument.map_data

    # return existing envelope with identical name
    for env in instrument.envelopes:
        if env == name:
            return instrument.envelopes[env]

    try:

        # get envelope data
        env = data["envelopes"][name]

        # merge envelope data with defaults
        env = config.merge_with_defaults(env, "envelopes")

        # load points
        points = env["points"]

        # skip if points isn't a list
        if not points or type(points) is not list:
            return None

        # store sustain setting
        sus = env["sustain"]

        # create envelope instance
        env_new = ref_env.Envelope(instrument, name, sus, points)

        # dynamic recalculation
        dynamic = env["dynamic"]
        env_new.dynamic = dynamic

        # return the created envelope
        return env_new

    except:
        return None

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add Variable via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def add_variable_via_lookup(instrument, name):

    import lib.classes.class_variable as ref_var
    import lib.config.config as config

    # load data
    data = instrument.map_data

    # return existing variable with identical name
    for var in instrument.variables:
        if var == name:
            return instrument.variables[var]

    try:

        # get variable data
        var = data["variables"][name]

        # merge variable data with defaults
        var = config.merge_with_defaults(var, "variable element")

        # create new variable
        var_new = ref_var.Variable(instrument, name)

        # return created variable
        return var_new

    except:
        return None

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add Curve via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~


def add_curve_via_lookup(instrument, name):

    import lib.classes.modulation.curve.class_curve as ref_crv
    import lib.config.config as config

    data = instrument.map_data

    # check if curve with identical name exists and reuse it
    for curve in instrument.curves:
        if curve == name:
            return instrument.curves[curve]

    # try implementing a curve
    try:
        # load curve data
        crv = data["curves"][name]

        # complete data with default values
        crv = config.merge_with_defaults(crv, "curve element")

        # curve attributes
        points = crv["points"]
        resolution = crv["resolution"]
        stepped = crv["steps"]

        # skip curves if they either aren't defined or not a list
        if not points or type(points) is not list:
            return None

        curve_new = ref_crv.Curve(instrument, name, "indexed", resolution, stepped)

        # go through curve points, construct curve
        for point in points:

            # add missing values
            if len(point) < 1:
                point.append(0)
            if len(point) < 2:
                point.append(1)
            if len(point) < 3:
                point.append(1)

            # add point to curve
            curve_new.add_point(point[0], point[1], point[2])

        # create curve (processing the points)
        curve_new.create()

        # return the created curve
        return curve_new

    except:
        # return nothing on fail
        return None


# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Method : Add LFO via Lookup
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

def add_lfo_via_lookup(instrument, name):

    import lib.classes.modulation.lfo.class_lfo as ref_flo
    import lib.config.config as config

    # load data
    data = instrument.map_data

    # return existing lfo with identical name
    for lfo in instrument.lfo:
        if lfo == name:
            return instrument.lfo[lfo]

    try:

        # get lfo data
        lfo = data["lfo"][name]

        # merge lfo data with defaults
        lfo = config.merge_with_defaults(lfo, "lfo")

        # load attributes
        waveform = lfo["waveform"]
        rate = lfo["rate"]
        delay = lfo["delay"]
        phase = lfo["phase"]
        fade = lfo["fade"]
        smooth = lfo["smooth"]
        offset = lfo["offset"]

        # modulation data
        mod_data = lfo["modulation"]

        # sub lfo data
        sub_lfo_data = lfo["sub"]

        # create lfo instance
        lfo_new = ref_flo.Lfo(instrument, name, sub_lfo_data, mod_data)

        # set attributes
        lfo_new.waveform.set_waveform(waveform)
        lfo_new.rate.depth = rate
        lfo_new.delay.depth = delay
        lfo_new.fade.depth = fade
        lfo_new.phase.depth = phase
        lfo_new.smooth.depth = smooth
        lfo_new.offset.depth = offset

        # return the created lfo
        return lfo_new

    except:
        return None

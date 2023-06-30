# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Range : Keyswitch
#
#   Represents a SFZ keyswitch
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..class_range import Range

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class KeySwitch(Range):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Get Global Range
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def get_sfz_global_range(instrument):

        # minimum and maximum bounds
        val_min = 127
        val_max = 0

        # keyswitch existence indicator
        has_keyswitch = False

        for part in instrument.parts:

            # get part instance
            part_inst = instrument.parts[part]

            # skip if no keyrange available
            if not part_inst.keyswitch:
                continue

            # store keyswitch
            ks = part_inst.keyswitch

            # get bounds
            ks_low = ks.get_range()[0]
            ks_high = ks.get_range()[1]

            # update bounds
            val_min = min(val_min, ks_low)
            val_max = max(val_max, ks_high)
            
            # there's a keyswitch
            has_keyswitch = True

        # don' return anything if there are no keyswitches
        if not has_keyswitch:
            return ""
        
        # construct sfz string
        data = ""
        data += "sw_lokey=" + str(val_min) + "\n"
        data += "sw_hikey=" + str(val_max) + "\n"
        
        try:
            ks = instrument.map_data["keyswitches"]["default"]
            data += "sw_default=" + str(instrument.keyswitches[ks].range_low) + "\n"
        except:
            data += "sw_default=" + str(val_min) + "\n"
        
        # return sfz string
        return data

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, part, label):

        super().__init__()

        # store part and instrument reference
        self.part = part
        self.instrument = self.part.instrument
        self.label = label

        # flag to indicate that program range is set
        self.program_set = False
        # program change range
        self.program_low = 0
        self.program_high = 127

        # store keyswitch in lookup table
        self.instrument.keyswitches[label] = self

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Program
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_program(self, low, high):
        # set range
        self.program_low = low
        self.program_high = high
        # mark program change as set
        self.program_set = True
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Attribute
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        data = ""

        # tonal keyswitch
        if self.is_set:
            # check if range is a single tone
            if self.range_low == self.range_high:
                # use loweest value
                data += "sw_last=" + str(self.range_low) + "\n"
            else:
                # use range for keyswitch
                data += "sw_lolast=" + str(self.range_low) + "\n"
                data += "sw_hilast=" + str(self.range_high) + "\n"
            data += "sw_label=" + str(self.label) + "\n"

        # program change keyswitch
        if self.program_set:
            data += "loprog=" + str(self.program_low) + "\n"
            data += "hiprog=" + str(self.program_high) + "\n"

        # return sfz string
        return data

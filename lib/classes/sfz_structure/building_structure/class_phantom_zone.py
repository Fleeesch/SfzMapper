# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Sfz Structure : Phantom Zone
#
#   Chain of Creation:
#   Builder > Instrument > Part > [Zone] > Split > Sound
#
#   Zone that is always silent and used for
#   creating effecte Choke Groups or triggering
#   specific scenarios that require a Voice Count
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.sfz_structure.building_structure.class_zone import Zone

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class PhantomZone(Zone):

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   Constructor
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def __init__(self, source):

        # part
        self.source = source

        try:
            # get note range directly from zone
            if isinstance(source, Zone):
                self.note_low = source.note_low
                self.note_high = source.note_high
            else:
                # try getting note range from elements zone
                self.note_low = source.zones[0].note_low
                self.note_high = source.zones[len(source.zones) - 1].note_high
        except:
            self.note_low = 0
            self.note_high = 127

        # append to source lookup list
        source.phantom_zone = self

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get SFZ
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz(self):

        data = ""

        # header tags
        data += "<region>" + "\n"
        data += "sample=*silence" + "\n"
        data += "trigger=attack" + "\n"

        # group numbers
        data += "group=" + str(self.source.group_off.get_index()) + "\n"
        data += "off_by=" + str(self.source.group_off.get_index()) + "\n"

        # note range
        data += "lokey=" + str(self.note_low) + "\n"
        data += "hikey=" + str(self.note_high) + "\n"

        return data

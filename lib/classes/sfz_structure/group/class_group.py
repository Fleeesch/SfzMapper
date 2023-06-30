# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Group
#
#   Represents an instance of a Choke Group.
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.classes.sfz_structure.building_structure.class_phantom_zone import \
    PhantomZone

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Group:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Add Group to Instrument
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def add_group_to_instrument(source, name, phantom_zone=True):
        # go through instruments group
        for group in source.instrument.groups:
            # group exists?
            if group.name.lower() == name.lower():
                # create phantom zone
                if phantom_zone:
                    PhantomZone(source)
                # return existing group
                return group
        
        # create a new group
        return Group(source, name, phantom_zone)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, source, name=None, phantom_zone=True):
        
        # store instrument
        self.source = source
        self.instrument = source.instrument

        # get group number from instrument group index
        self.group_nr = self.instrument.group_index

        # increment instrument group index
        self.instrument.group_index += 1
        
        # add group to instrument group list
        self.instrument.groups.append(self)

        # phantom zone
        if phantom_zone:
            source.phantom_zone = PhantomZone(source)
        
        if name is not None:
            self.name = name
        else:
            self.name = "Group" + str(self.group_nr)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Index
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def get_index(self):
        return self.group_nr

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Phatom Region
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_sfz_phantom_region(self):

        if self.phantom_region is None:
            return ""

        return self.phantom_region.get_sfz()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Config : External
#
#   External Configuration file, for storing
#   permanent data (mostly GUI related)
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from configparser import ConfigParser

from lib import message

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class ConfigExternal:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Statich Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    path_header = "PATH"

    path_count = "COUNT"

    path_list = [
        "Path A",
        "Path B",
        "Path C",
        "Path D",
        "Path E",
        "Path F",
        "Path G",
        "Path H",
        "Path I",
        "Path J"
    ]

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, filename="config.ini"):

        # create instance
        self.cp = ConfigParser()

        # store filename
        self.filename = str(filename)

        # 'config is setup' flag
        self.config_ok = False

        # load the config
        self.load_config()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Load Config
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_config(self):

        # try loading the config
        try:
            # open file to eventually throw error
            open(self.filename, "r")

            # read file intro config
            self.cp.read(self.filename)

            # mark config as read
            self.config_ok = True
        except:

            # load default values
            self.load_defaults()

            # save config file
            self.save_config()

            # mark config read as ok
            self.config_ok = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Write Data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def write_data(self, header, address, data):

        # only write if config exists
        if not self.config_ok:
            return

        try:
            # check if header exists
            self.cp[header]
        except:
            # create one if there's no header
            self.cp[header] = {}
        
        # store data in config instance
        self.cp[header][address] = data

        # save config
        self.save_config()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Get Data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_data(self, header, address):
           
        # don't get data if config isn't initialized
        if not self.config_ok:
            return None
        
        # get data
        return self.cp[header][address]
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Store Path
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def store_path(self, index, path):

        # write data
        self.write_data(ConfigExternal.path_header, ConfigExternal.path_list[index], path)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Get Path
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_path(self, index):

        # return data
        return self.get_data(ConfigExternal.path_header, ConfigExternal.path_list[index])

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Store Path Count
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def store_path_count(self, count):

        # write data
        self.write_data(ConfigExternal.path_header, ConfigExternal.path_count, count)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: get Path Count
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_path_count(self):

        # return data
        return self.get_data(ConfigExternal.path_header, ConfigExternal.path_count)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Save Config
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def save_config(self):

        # try saving conifg
        try:
            with open(self.filename, 'w') as f:
                self.cp.write(f)
        except:
            message.error("Couldn't write Settings to " + self.filename)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method: Get Defaults
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_defaults(self):

        # directly store default settings

        # setup folder path dict
        self.cp[ConfigExternal.path_header] = {}
        
        # create empty paths
        for entry in ConfigExternal.path_list:
            self.cp[ConfigExternal.path_header][entry] = ""

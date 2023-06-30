# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Builder
#
#   Chain of Creation:
#   [Builder] > Instrument > Part > Zone > Split > Sound
#
#   Processor of a YAML mapping file,
#   Contains instruments that are to be processed
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
from glob import glob

from lib import message, settings
from lib.config import config

from .building_structure.class_instrument import Instrument

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Builder:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # lookup table for instances
    lookup = []

    # assume there are no builers by default
    is_empty = True

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   Static Method : Write Sfz Files
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def write_sfz_files():

        # start with empty sfz file count
        message.reset_sfz_count()

        # go through instrument
        for ins in Instrument.lookup:

            # increment sfz file count
            message.increment_sfz_count()

            try:
                # progress message
                message.progress("+ " + ins.generate_sfz_name())

                # write the sfz fail
                ins.write_sfz_file()

                # success line end
                message.success()
            except:
                # fail line end
                message.fail()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   Static Method : Setup Builders from Base Path
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # [!]
    # The mapping process starts here and moves
    # hierarchically inwards torwards the smaller elements

    @staticmethod
    def setup_builders_from_path(path=""):

        # skip entire process if path is not valid
        if not path:
            return

        # empty lookup table
        Builder.lookup = []

        # clear instrument lookup
        Instrument.clear_lookup()

        # assume there are no builders
        Builder.is_empty = True
        
        # lookup yaml file names
        name_yml = settings.MAP_NAME + ".yml"
        name_yaml = settings.MAP_NAME + ".yaml"
        
        # go trhough full directory tree
        for dir, _, _ in os.walk(path):
            
            # try getting a proper yaml file, create instruments from it
            try:
                
                file_yml = dir + "/" + name_yml
                file_yaml = dir + "/" + name_yaml
                
                file_path = ""
                
                # cehck if yml or yaml file is available, store path
                if os.path.isfile(file_yml):
                    file_path = file_yml
                elif os.path.isfile(file_yaml):
                    file_path = file_yaml
                
                # skip file if not valid
                else:
                    continue
                
                # file found, setup builder
                Builder.setup_builder_from_file(file_path)
                
                # print individual mapping summary
                message.mapping_summary()
            except:
                # generic error message
                message.error("Something went wrong during the building process")
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    #   Static Method : Setup Builder from Path
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    @staticmethod
    def setup_builder_from_file(file_path=""):
        
        # skip empty paths
        if not file_path:
            return
        
        # get path and file from string
        path = os.path.dirname(file_path)
        file = os.path.basename(file_path)
        
        # make sure to only load yamls
        if file != "map.yml" and file != "map.yaml":
            return
        
        # info message
        message.map_found(file, path)
        
        # setup builder
        return Builder(path, file)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def __init__(self, path, file):
        
        # store path and file
        self.map_path = path
        self.map_file = file
        self.map_abs = path + "/" + file
        
        # full yaml file
        self.map_data_global = {}
        
        # raw map data
        self.map_data = {}
        
        # instruments
        self.instruments = {}
        
        # writers
        self.writers = []
        
        # load basic settings
        self.load_settings()
        
        # add to lookup list
        Builder.lookup.append(self)
        
        # notice that there are builders
        Builder.is_empty = False
        
        # go through instrument data
        for idx, ins in enumerate(self.map_data["instruments"]):
            
            # instrument addition line
            message.info("+ Instrument " + ins)
            message.indent()
            
            # try creating instrument from data
            try:
                Instrument.create(self, ins)
                
                # inform of successful build
                message.instrument_end_line("Instrument successfully built.")
            
            except:
                # inform of build failure
                message.instrument_end_line("Something went wrong when building the instrument", True)
    
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Settings
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def load_settings(self):
        
        
        # store data from map file
        self.map_data_global = config.load_yaml(self.map_abs)
        
        # try setting up local templates
        config.setup_local_templates_from_builder(self)
        
        # try applying placeholders
        placeholder_tempfile = config.fill_placeholders(self)
        
        # temporary file for placeholders exists? Load it instead!
        if placeholder_tempfile:
            self.map_data_global = config.load_yaml(placeholder_tempfile)
            
        # store data from map file
        self.map_data = self.map_data_global["sfz"]
        
        # merge with defaults
        self.map_data = config.merge_with_defaults(self.map_data, "sfz")
        
        # insert snippets
        config.insert_snippets(self.map_data)
        
        # copy instrument on request
        config.copy_section(self.map_data, "instruments")
        
        # copy parts on request
        config.copy_section(self.map_data, "parts")
        
        # cleanup temp files
        config.remove_temp_files(self.map_path)        

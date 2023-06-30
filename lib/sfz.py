# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : SFZ
#
#   Single purpose module for mapping SFZ files
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os

from lib import message
from lib.classes.sfz_structure.class_builder import Builder
from lib.config import config
from lib import lookup

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Globals
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# indicator of ongoing mapping process
MAPPING_BUSY = False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load Ressources
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# [!]
# Loads configuration files that are absolutely
# integral to the functionality of the mapping process


def load_ressources():
    

    # info line about loading ressources
    message.info("Loading Ressources...")
    message.linebreak()
    message.indent()

    # load default settings, abort everything on exit
    try:
        config.load_default_settings()
    except:
        # fatal error, missing defaults always leads to exit
        message.error_fatal("Couldn't load default settings")

    # load templates and default settings
    try:
        config.load_templates()
    except:
        # Generic error message
        message.error("Couldn't load templates")

    # print summary, add some space
    message.ressource_summary()
    message.indent_back()
    message.linebreak()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Make SFZ
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# [!]
# Starting point of the mapping process,
# call this method with a valid path to look through
# the folder structure for mapping files and process them


def make_sfz(path_abs):

    global MAPPING_BUSY

    # skip if mapping is already in process
    if MAPPING_BUSY:
        return
    
    # reset counters in messages
    message.reset_sfz_count()
    message.reset_error_count()
    message.reset_total_error_count()
    
    # skip if path isn't valid
    if not os.path.isdir(path_abs):
        return
    
    # mark mapping process as busy
    MAPPING_BUSY = True
    
    
    # generate date string to be used across instruments
    lookup.generate_data_string()
    
    # clear message output, print introduction message
    message.clear_output()
    
    # load configuration data
    load_ressources()
    
    # inform about search for mapping files
    message.info("Looking for Mapping files...")
    message.linebreak()

    # try initiating the mapping process by starting with the builders
    try:
        # setup builders from base path
        Builder.setup_builders_from_path(path_abs)

        # print summary message of mapping process
        message.mapping_summary_total()

    except:
        # generic error message
        message.error("Something went wrong when trying to setup Builders")

    # start SFZ writing process only if builders exist
    if not Builder.is_empty:

        try:
            # remove previous formatation
            message.reset_error_count()
            message.indent_reset()
            message.linebreak()

            # print introductionary line
            message.info("Writing SFZ files...")
            message.indent()

            # write sfz files
            Builder.write_sfz_files()

            # print writing process summary
            message.writing_summary()

        except:
            # generic error message
            message.error("Something went wrong when writing a SFZ file")

    # mapping done
    MAPPING_BUSY = False

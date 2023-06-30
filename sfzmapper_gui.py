# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   SFZ Mapper
#   (GUI Version)
#
#   Automatic SFZ-Instrument Creator
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import atexit

from lib import version
from lib.config import config
from lib.gui.class_gui import Gui

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : At Exit
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def at_exit():

    config.remove_temp_files()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Setup
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# load version
version.load_version()

# store source folder
config.store_source_folder()

# load external config
config.setup_external_config()

# activate GUI
Gui()

# register on-exit methods
atexit.register(at_exit)

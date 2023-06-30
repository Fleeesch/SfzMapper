# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   SFZ Mapper
#   (CLI Version)
#
#   Automatic SFZ-Instrument Creator
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import gc
import os
import sys

from lib import message, sfz

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Setup
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# get arguments
arguments = sys.argv

# * * * * * * * * * * * * * * * * * *
# Exception Class : Argument Count Error


class CountError(Exception):
    genericmessage = "Missing Argument for Directory"

# * * * * * * * * * * * * * * * * * *
# Exception Class : Path Error


class PathError(Exception):
    genericmessage = "Path is not a directory"


# Try creating SFZ files
try:
    
    # get folder from first argument
    dir = arguments[1]
    
    # first argument needs to be available
    if len(arguments) < 1:
        raise CountError
    
    # check if path is valid
    if os.path.isdir(dir):
        # create sfz
        sfz.make_sfz(dir)
    
    else:
        raise PathError

# error messages
except CountError as e:
    message.error_fatal(e.genericmessage)
except PathError as e:
    message.error_fatal(e.genericmessage)
except:
    pass

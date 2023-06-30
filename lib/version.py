# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Version
#
#   For gathering Versioning-Data
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Globals
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

VERSION = "1.0"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Store Verion
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def store_version():

    global VERSION

    with open("version", "w", encoding="latin-1") as f:

        f.write(VERSION)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Load Version
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def load_version():
    
    global VERSION
    
    # try opening version file
    try:
        with open("version", "r") as f:
            
            # store version string
            VERSION = f.read()
    
    except:
        
        # store version if file doesn't exist
        VERSION = "1.0"
        store_version()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Get Version
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_version_string():

    return "v" + VERSION

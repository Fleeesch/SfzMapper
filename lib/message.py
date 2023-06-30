# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Messages
#
#   For displaying Terminal / Infobox Messages
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
from random import randint

from lib.classes.sfz_structure.class_builder import Builder
from lib.gui.output.class_gui_output import GuiOutput

from . import settings
from lib import version

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Globals
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# reference to existing GUI
GUI = None

# indent
MESSAGE_INDENT = 0

# temporary error count for local mapping process of a map.yml
ERROR_COUNT = 0

# error count for complete mapping process
ERROR_COUNT_TOTAL = 0

# counts sfz files that need to be written
SFZ_COUNT = 0

# tab space
TAB = "    "

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Increment SFZ Count
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def increment_sfz_count():
    
    global SFZ_COUNT
    
    SFZ_COUNT += 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reset SFZ Count
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reset_sfz_count():

    global SFZ_COUNT

    SFZ_COUNT = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Disable Output
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def disable_output():

    settings.MESSAGE_OFF = True

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Enable Output
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def enable_output():

    settings.MESSAGE_OFF = False

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Indent
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def indent():

    global MESSAGE_INDENT

    # increment indent
    MESSAGE_INDENT += 1

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reset Indent
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def indent_reset():

    global MESSAGE_INDENT

    # reset indent
    MESSAGE_INDENT = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reverse Indent
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def indent_back():

    global MESSAGE_INDENT

    # decrement
    MESSAGE_INDENT -= 1

    # indent must not be smaller than 0
    if MESSAGE_INDENT < 0:
        MESSAGE_INDENT = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Get Indet
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def indent_get():

    global MESSAGE_INDENT

    # return string
    data = ""

    # add tabs
    for i in range(0, MESSAGE_INDENT):
        data += TAB

    # return data
    return data

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Clear Output
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def clear_output():

    # reset indentation
    indent_reset()

    # clear output of gui textbox
    if GUI:
        GUI.clear_output()

    # clear terminal
    if not GUI or settings.MESSAGE_ALWAYS_PRINT_TO_TERMINAL:
        os.system('cls' if os.name == 'nt' else 'clear')


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Fatal Error
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def error_fatal(msg=""):

    # local color tag
    tag = GuiOutput.COLOR_TAG_ERROR

    # separator line
    line()
    separator(tag)

    # create universal message if no message has been given
    if not msg:
        output("FATAL ERROR: Aborting Process", False, tag)
    else:
        output("FATAL ERROR: " + msg + ", aborting Process", False, tag)

    # wait for input
    input(indent_get() + "Press any Key to exit...")

    # stop the software
    exit()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reset Error Count
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reset_error_count():
    
    global ERROR_COUNT
    
    ERROR_COUNT = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reset Total Error Count
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
def reset_total_error_count():
    
    global ERROR_COUNT_TOTAL
    
    ERROR_COUNT_TOTAL = 0

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Map Found Line
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def map_found(line_a="", line_b=""):

    tag = GuiOutput.COLOR_TAG_REMARK

    indent_reset()
    shallow_line(tag)

    info("Found " + line_a + " in...\n" + line_b, tag)

    linebreak()
    indent()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Instrument End Line
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def instrument_end_line(msg="", has_error=False):

    # set default tag
    tag = GuiOutput.COLOR_TAG_SUCCESS

    # error tag
    if has_error:
        tag = GuiOutput.COLOR_TAG_ERROR

    # underline
    line(tag)

    # print instrument build info
    if has_error:
        error(msg)
    else:
        info(msg, tag)

    # go back with indentation
    indent_back()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Ressource Summary
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def ressource_summary():

    global ERROR_COUNT

    # default tag
    tag = GuiOutput.COLOR_TAG_SUCCESS

    # error tag
    if ERROR_COUNT:
        tag = GuiOutput.COLOR_TAG_ERROR

    # separation
    linebreak()
    separator(tag)

    # open line
    output(TAB + "Ressources loaded", False, tag)

    # output error count or nothing
    if ERROR_COUNT:

        # line end
        output(": " + str(ERROR_COUNT) + " Errors!", True, tag)
    else:

        # line end / break
        output()

    # separator line
    separator(tag)

    # reset local error count
    reset_error_count()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Mapping Summary
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def mapping_summary():

    global ERROR_COUNT

    # default tag
    tag = GuiOutput.COLOR_TAG_SUCCESS

    # error tag
    if ERROR_COUNT:
        tag = GuiOutput.COLOR_TAG_ERROR

    # space
    linebreak()

    # print optional error count
    if not ERROR_COUNT:
        output("Map Complete.", True, tag)
    else:
        output("Map Complete: " + str(ERROR_COUNT) + " Errors!", True, tag)
    
    # reset local error count
    reset_error_count()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Linebreak
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def linebreak():

    # empty output always creates linebreak
    output()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Line
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def line(tag=None):

    # indented line
    output(indent_get() + "- - - - - - - - - - - - - - - - - -", True, tag)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Separator
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def separator(tag=None):

    output("-------------------------------------------------------------------", True, tag)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Shallow Line
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def shallow_line(tag=None):

    output(". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .", True, tag)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Total Mapping Summary
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def mapping_summary_total():

    global ERROR_COUNT_TOTAL

    # default tag
    tag = GuiOutput.COLOR_TAG_SUCCESS

    # error tag
    if Builder.is_empty:
        tag = GuiOutput.COLOR_TAG_REMARK
    elif ERROR_COUNT_TOTAL:
        tag = GuiOutput.COLOR_TAG_ERROR

    # separation
    linebreak()
    separator(tag)

    # start of finishing line
    output(TAB + "Mapping Done", False, tag)

    # special message if there or no mappings
    if Builder.is_empty:
        output(": Couldn't find any Mapping files", True, tag)

    # print total errors if there are any
    elif ERROR_COUNT_TOTAL:
        output(": " + str(ERROR_COUNT_TOTAL) + " Errors!", True, tag)

    # neutral message
    else:
        output()
    
    # reset total error count
    reset_total_error_count()
    
    # separator endline
    separator(tag)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Writing Summary
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def writing_summary():

    global ERROR_COUNT

    # default tag
    tag = GuiOutput.COLOR_TAG_SUCCESS

    # remark when there is no sfz count
    if not SFZ_COUNT:
        tag = GuiOutput.COLOR_TAG_REMARK
    # error tag
    elif ERROR_COUNT:
        tag = GuiOutput.COLOR_TAG_ERROR

    # separataor
    linebreak()
    separator(tag)

    if not SFZ_COUNT:
        output(TAB + "No SFZ files to create", True, tag)
    else:

        # finishing line
        output(TAB + "SFZ Files created", False, tag)

        # print local errors if there were any

        if ERROR_COUNT:
            output(": " + str(ERROR_COUNT) + " Errors!", True, tag)
        else:
            output()

    # separator line
    separator(tag)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Error
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def error(msg=""):

    global ERROR_COUNT, ERROR_COUNT_TOTAL

    # increment error count
    ERROR_COUNT += 1
    ERROR_COUNT_TOTAL += 1

    # don't print error messages if told to do so
    if not settings.MESSAGE_PRINT_ERROR:
        return

    # output message with error preamble
    output(indent_get() + "ERROR: " + msg, True, GuiOutput.COLOR_TAG_ERROR)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Fail
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def fail():

    # don't print details if told to do so
    if not settings.MESSAGE_PRINT_INFO:
        return

    # add "error" to the end of a line
    output("ERROR!", True, GuiOutput.COLOR_TAG_ERROR)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Success
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def success():

    # don't print details if told to do so
    if not settings.MESSAGE_PRINT_INFO:
        return

    # add "ok" to the end of a line
    output("OK", True, GuiOutput.COLOR_TAG_SUCCESS)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Progress
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def progress(msg=""):

    # don't print details if told to do so
    if not settings.MESSAGE_PRINT_INFO:
        return

    if not msg:
        return

    output(indent_get() + msg + "... ", False)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Info
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def info(msg="", tag=None):

    if not settings.MESSAGE_PRINT_INFO:
        return

    if not msg:
        return

    output(indent_get() + msg, True, tag)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Print Info
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def remark(msg=""):

    if not settings.MESSAGE_PRINT_INFO:
        return

    if not msg:
        return

    output(indent_get() + "? " + msg + " ...", True, GuiOutput.COLOR_TAG_REMARK)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Welcome Message
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def welcome_message():

    # list of possible welcome lines
    welcome_lines = [
        "Squeezing all the juice out of\ndated SoundFonts since 2023",
        "The most complicated way of making\nthe most cheap-ass MIDI sounds",
        "Thousand lines of code for\ntwo lines of modulation",
        "Crossfading crossfades,\nModulating modulators!"
    ]

    # get random welcome line
    welcome_line = welcome_lines[randint(0, len(welcome_lines) - 1)]

    # separate welcome message by lines
    lines = welcome_line.split("\n")

    linebreak()

    # header
    info(TAB + "SFZ MAPPER " + version.get_version_string())

    linebreak()

    # print welcome message line by line with tab
    for line in lines:
        info(TAB + line)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Output
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def output(msg="", linebreak=True, tag=None):

    global GUI

    # don't print anything if output is disabled
    if settings.MESSAGE_OFF:
        return

    # if a GUI is available forward mesage torwards GUI
    if GUI:
        if tag:
            GUI.print_message(msg, linebreak, tag)
        else:
            GUI.print_message(msg, linebreak)

    # print message to terminal (ignore if GUI gets exclusive output)
    if not GUI or settings.MESSAGE_ALWAYS_PRINT_TO_TERMINAL:
        print(msg)

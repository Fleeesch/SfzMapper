# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Config : Reformat : SFZ
#
#   Functionality for formatting SFZ files once
#   their content has been created
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Reformat SFZ
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def reformat_sfz(data):

    # reformatted string
    data_new = ""

    symbol_line_placeholder = config.DEFAULTS["sfz"]["symbols"]["line placeholder"]
    symbol_comment_line_placeholder = config.DEFAULTS["sfz"]["symbols"]["comment line placeholder"]

    # - - - - - - - - - - - - - - - -
    #   Remove Blank Lines

    # split lines
    lines = data.split("\n")

    # go through lines
    for line in lines:

        # skip emtpy lines
        if not line:
            continue

        # line placeholder empties line
        if symbol_line_placeholder in line:
            line = ""
        
        if symbol_comment_line_placeholder in line:
            line = "//"

        # add line to new data string
        data_new += line + "\n"

    # split lines again
    lines = data_new.split("\n")

    # comment lookup array for lines
    comment = [False] * len(lines)

    # - - - - - - - - - - - - - - - -
    #   Mark Comments

    # go through lines to find comments
    for idx, line in enumerate(lines):

        # mark line as comment
        if "//" in line:
            comment[idx] = True

    # return string
    data_new = ""

    # - - - - - - - - - - - - - - - -
    #   Add Spaces

    # go through lines
    for idx, line in enumerate(lines):

        # strip whitespace
        line = line.strip()

        # add extra linebreak when...
        # previous comment is a conventional line and not empty
        # next line is a comment
        if idx > 0:
            if not comment[idx - 1] and lines[idx - 1] and comment[idx]:
                data_new += "\n"

        # add line
        data_new += line + "\n"

    # return formatted string
    return data_new

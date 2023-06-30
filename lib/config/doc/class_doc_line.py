# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Documentary : Line
#
#   Filters Meta Data from a Line
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class DocLine:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, line, block_comment=False):

        # flag for ignoring the line for output
        self.ignore = False

        # flag to indicate an opening / closing block comment
        self.block_comment_tag = False

        # comment printed within a list
        self.list_comment = False

        # comment line header
        self.comment_header = False

        # comment that desevers attention marking
        self.comment_attention = False

        # indicator that line is part of a block comment
        self.block_comment = block_comment

        # get output line from input line
        self.output = str(line)

        # assume level is 0 by default
        self.level = 0

        # ::::::::::::::::::::::::::::::
        #   Filtering
        # ::::::::::::::::::::::::::::::

        # yaml file initial line
        if line.strip() == "---":
            self.output = ""
            self.ignore = True
            return

        # empty lines
        if not line.strip():
            self.output = ""
            self.ignore = True
            return

        # inmplement header tag
        if "[h]" in self.output:
            self.comment_header = True
            self.output = self.output.replace("[h]", "")

        if "[!]" in self.output:
            self.comment_attention = True
            self.output = self.output.replace("[!]", " * ")

        # lines that open / close a block comment
        if '#--' in self.output:
            self.block_comment_tag = True
            return

        if "##" in line.strip():
            self.list_comment = True

        # lines starting with a comment
        elif line.strip()[0] == "#" and not block_comment:
            self.output = ""
            self.ignore = True
            return

        # ::::::::::::::::::::::::::::::
        #   Attributes
        # ::::::::::::::::::::::::::::::

        # get leading spaces
        leading_space = len(line) - len(line.lstrip())

        # store level from leading spaces
        self.level = round(leading_space / 2)

        # position of inline-comment substring
        comment_inline_pos = -1

        # inline-comment
        comment_inline = ""

        # ::::::::::::::::::::::::::::::
        #   Inline Comments
        # ::::::::::::::::::::::::::::::

        # check for a comment mark
        if "# " in self.output:
            for idx, char in enumerate(self.output):

                # store comment position
                if char == "#":
                    comment_inline_pos = idx
                    break

        # inline-comment found?
        if comment_inline_pos >= 0:

            # store comment
            comment_inline = self.output[comment_inline_pos + 2:]

            # keep comment padding for specific comment elements
            if block_comment or self.list_comment:

                # keep spaces
                comment_inline = comment_inline.replace(" ", "&nbsp;")

            # store line without comment
            self.output = self.output[0:comment_inline_pos]

            # comment bracket attribute position
            bracket_pos = -1

            # check for first bracket in comment
            if "[" in comment_inline:
                for idx, char in enumerate(comment_inline):

                    # store bracket position
                    if char == "[":
                        bracket_pos = idx
                        break

            # comment bracket attribute found?
            if bracket_pos >= 0:

                # store part of the comment that starts with the bracket
                sub_comment = comment_inline[bracket_pos:]

                # construct comment with bracket attribute
                comment_inline = comment_inline[0:bracket_pos] + '<span class="highlight">' + sub_comment + '</span>'

            # construct comment
            comment_inline = '<span class="comment">' + comment_inline + '</span>'

        # ::::::::::::::::::::::::::::::
        #   Output
        # ::::::::::::::::::::::::::::::

        # replace remaining comment symbols
        self.output = self.output.replace("#", "")

        # arrow symbol of inline comment
        comment_inline = comment_inline.replace("<--", "&larr;")

        # only strip output if not part of a block comment
        if not block_comment:
            # merge output with comment
            self.output = self.output.strip() + "  " + comment_inline
        else:
            # use comment line
            self.output = comment_inline

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Get
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get(self):
        # return output string
        return self.output

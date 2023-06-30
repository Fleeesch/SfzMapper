# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Structure : Entry
#
#   Basic entry of the content section.
#   Every other type of entry is an extension of this class.
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..lookup import lookup


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Entry:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, structure):
        from .class_entry_section import Section

        # structure reference
        self.structure = structure

        # indent level
        self.level: int = 0

        # raw file string
        self.line: str = ""

        # id appendix for unique identification
        self.id_appendix: str = ""

        # unique identifier
        self.id: str = ""

        # section indicator
        self.is_section = False

        self.line_no_comment: str = ""
        self.comment_inline: str = ""

        self.line_value: str = ""
        self.line_no_value: str = ""

        # yaml comment flags
        self.is_empty: bool = False
        self.is_full_line_comment: bool = False
        self.has_comment: bool = False
        self.has_inline_comment: bool = False
        self.has_value: bool = False
        self.is_file_reference: bool = False
        self.value_only = False

        # reference to potential parent section
        self.parent_section: Section | None = None

        # 1st level entry flag
        self.is_root_entry: bool = False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set ID Appendix
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_id_appendix(self, val: str = ""):
        self.id_appendix = val

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Detect Empty Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def detect_empty_line(self):
        if self.line.strip() == "":
            self.is_empty = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Detect Comment
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def detect_comment(self):

        # Full-Line Comment
        if self.line.strip().startswith("#"):
            self.is_full_line_comment = True

        # Comment Appearance
        if self.line.lstrip().find(" # ") > 0:
            self.has_comment = True

        # Inline Comment
        if self.has_comment and not self.is_full_line_comment:
            self.has_inline_comment = True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Level
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_level(self, level: int):
        self.level = level

        # raise flag in case entry is on root level
        self.is_root_entry = (self.level <= 0)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_line(self, line: str = ""):

        # store line
        self.line = line
        self.line_no_comment = line.strip()
        self.line_no_value = self.line_no_comment

        # detect line attributes
        self.detect_empty_line()
        self.detect_comment()

        # filter inline comment
        if self.has_inline_comment:
            line_parts = self.line.split(" # ")

            self.comment_inline = line_parts[-1].strip()
            self.line_no_comment = self.line[:-(len(line_parts[-1]) + 2)]

        # no attribute, only value (bullet lists)
        if not self.is_full_line_comment and not ":" in self.line_no_comment:
            self.value_only = True

        # store line separated from value
        try:
            split_lines = self.line_no_comment.split(":")
            self.line_no_value = split_lines[0]
            self.line_value = split_lines[1]

        except:
            pass

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Parent Section
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_parent_section(self, section):
        self.parent_section = section

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : set ID
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_id(self, id):
        self.id = id

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Format
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def format(self):

        from ..class_converter import Converter

        if self.has_inline_comment:
            self.comment_inline = Converter.apply_markdown(self.comment_inline)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Section
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_section(self) -> str:
        return self.get_html_line()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get HTML Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_line(self) -> str:

        # return line
        line = ""

        # return nothing when a "blank" attribute is given
        # if self.line_no_value.lower() == "blank":
        #    return ""

        # create and store individual id
        id_str = f'{self.line_no_comment.replace(":", "").strip()}'
        id_str = id_str.replace(" ", "")

        # add optional id appendix
        if self.id_appendix:
            id_str += f'@{self.id_appendix}'

        # set custom id
        self.set_id(id_str)

        # default click action
        click_action = lookup.js_method_copy

        # remove click action from value only and file references
        if self.value_only or self.is_file_reference:
            click_action = ""

        # div container line
        line += f'<div ' \
                f'onclick="{click_action}" ' \
                f'class="{lookup.html_class_line_wrapper} {lookup.html_class_level}-{self.level}" '

        # add id for root entries, just close tag if not
        if self.is_root_entry:
            line += f'id="{id_str}">'
        else:
            line += f'>'

        # entry is a section header
        if self.is_section:

            line += f'<span class="' \
                    f'{lookup.html_class_section} ' \
                    f'{lookup.html_class_attribute}">' \
                    f'{self.line_no_comment}' \
                    f'</span>'

        # entry is a conventional line
        else:

            # differentiate between entries that have a value and
            # those who don't
            if not self.value_only:

                line += f'<span class="' \
                        f'{lookup.html_class_attribute} ' \
                        f'">' \
                        f'{self.line_no_value}:' \
                        f'</span>' \
                        f'<span class="' \
                        f'{lookup.html_class_value} ' \
                        f'">' \
                        f'{self.line_value}' \
                        f'</span>'

            else:

                line += f'<span class="' \
                        f'{lookup.html_class_attribute} ' \
                        f'">' \
                        f'</span>' \
                        f'<span class="' \
                        f'{lookup.html_class_value} ' \
                        f'">' \
                        f'{self.line_no_comment}' \
                        f'</span>'

        # optional inline comment
        if self.has_inline_comment:
            line += " "

            line += f'<span class="' \
                    f'{lookup.html_class_comment} ' \
                    f'{lookup.html_class_comment_inline}' \
                    f'">' \
                    f'{self.comment_inline}' \
                    f'</span>'

        line += "</div>"

        return line

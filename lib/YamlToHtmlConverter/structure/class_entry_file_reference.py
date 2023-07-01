# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Structure : Entry : File Reference
#
#   A line representing information about a file.
#   Used as a separation header whenever a new file section begins.
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..lookup import lookup
from .class_entry import Entry


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class FileReference(Entry):

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, structure, file):
        super().__init__(structure)

        from ..file.class_filehandler import FileHandler

        # declare itself as file reference
        self.is_file_reference = True

        # store file
        self.file: FileHandler = file

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get  HTML Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_html_line(self) -> str:
        line = ""

        class_first_entry = ""

        if self.structure.file_handler[0] == self.file:
            class_first_entry = "first-file-entry"

        # line-wrapping div container
        line += f'<div ' \
                f'class="{lookup.html_class_line_wrapper} {lookup.html_class_level}-0 ' \
                f'{lookup.html_class_file_reference} {class_first_entry}" ' \
                f'id="{self.file.file_name}{self.file.file_extension}" ' \
                f'<span>{self.file.file_name}{self.file.file_extension}</span>' \
                f'</div>'

        return line

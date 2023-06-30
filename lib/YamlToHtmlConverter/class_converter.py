# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Converter
#
#   Main Communicator between the classes.
#   Contains everything necessary for a conversion process.
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os
import re
import textwrap
import webbrowser
from datetime import datetime

from .file.class_filehandler import FileHandler
from .lookup import lookup
from .structure.class_structure import Structure


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Converter():

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Create
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    @staticmethod
    def create(file: str | list[str], html: str):

        # convert to list
        if not isinstance(file, list):
            file = [file]

        # check for valid files
        for f in file:

            # remove not exiting files
            if not os.path.exists(f):
                file.remove(f)
                break

            file_name, file_extension = os.path.splitext(os.path.basename(f))

            # remove non-yaml files
            if file_extension not in [".yaml", ".yml"]:
                file.remove(f)
                break

        # skip if there are no files
        if not file:
            return None

        # create a converter, return its instance
        return Converter(file, html)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Insert Symbols
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def insert_symbols(input_str: str) -> str:

        for smb in lookup.markdown_symbols:
            new_line = f'<span class="{lookup.markdown_symbols[smb]}"></span>'
            input_str = input_str.replace(smb, new_line)

        return input_str

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Apply Markdown
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def apply_markdown(line: str) -> str:

        # ------------------------------
        #   Sub-Method : Apply RegEx
        # ------------------------------
        def apply_regex(input_str: str, class_name: str, tag_open: str, tag_close: str | None = None) -> str:

            if not tag_open:
                return input_str

            new_str = f'<span class="{class_name}">\\1</span>'

            if tag_close:
                regex = f'{re.escape(tag_open)}(.*?){re.escape(tag_close)}'
            else:
                regex = f'{re.escape(tag_open)}(.*?)$'

            return re.sub(regex, new_str, input_str)

        # ------------------------------

        # go through markdown entries
        for markdown in lookup.markdown:
            md = lookup.markdown[markdown]

            if len(md) > 1:
                line = apply_regex(line, markdown, md[0], md[1])
            else:
                line = apply_regex(line, markdown, md[0])

        return line

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, file: list[str], html: str):

        # html file about to be created
        self.html_file = html

        # flag to inform you that the building process went ok
        self.build_success = False

        # declare file handler list
        self.file_handler: list[FileHandler] = []

        # add file handlers
        for f in file:
            self.file_handler.append(FileHandler(self, f))

        # create structure
        self.structure: Structure = Structure(self)

        # unique ID make from timestamp
        self.id = self.generate_version_id()

        # make html file
        self.create_html()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Generate Version ID
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def generate_version_id(self) -> str:
        return datetime.now().strftime("%Y%m%d%H%M%S") + str(datetime.now().microsecond)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Open HTML
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def open_html(self):

        # get absolute path
        abs_path = os.path.abspath(self.html_file)

        # skip if file doesn't exist
        if not os.path.exists(abs_path):
            return

        # open file in web browser
        webbrowser.open(abs_path)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create HTML
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create_html(self):

        # -----------------------------
        #   Sub-Method : Add Checkbox
        # -----------------------------

        def add_checkbox(id, label):

            return f"""
                    <input type="checkbox" id="{id}" 
                    class="{lookup.html_class_settings_checkbox}"  
                    onchange="{lookup.js_method_checkbox_change}" 
                    checked="true">
                    <label for="{id}" 
                    class="{lookup.html_class_settings_checkbox_label}">
                    {label}
                    </label>
                    """

        # -----------------------------

        # checkboxes
        html_checkbox_comment_blocks = add_checkbox(lookup.html_id_check_comment_blocks, "Block Comments")
        html_checkbox_comments = add_checkbox(lookup.html_id_check_comments, "Inline Comments")
        html_checkbox_values = add_checkbox(lookup.html_id_check_values, "Values")
        html_checkbox_code = add_checkbox(lookup.html_id_check_code, "Code")
        html_checkbox_hints = add_checkbox(lookup.html_id_check_hints, "Hints")
        html_checkbox_warnings = add_checkbox(lookup.html_id_check_warnings, "Warnings")

        # header start
        html_header = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                        <title>{self.file_handler[0].file_name.capitalize()}</title>
                        <link rel="stylesheet" href="styles.css?v={self.id}">
                        </head>
                        <body>
                        """

        html_input_filter = f"""
                        <input type="text" id="{lookup.html_id_filter}" 
                        onkeyup="{lookup.js_method_filter_input}" 
                        placeholder="Filter...">    
                        """

        html_settings = f"""
                    <div id="{lookup.html_id_settings_bar}"> 
                    <div id="{lookup.html_id_settings_bar_grid_container}">
                    <div id="{lookup.html_id_filter_wrapper}" class="{lookup.html_class_settings_bar_grid_element}"> 
                    {html_input_filter} </div>
                    <div class="flex{lookup.html_class_settings_bar_grid_element}">
                    {html_checkbox_comment_blocks} </div> 
                    <div class="{lookup.html_class_settings_bar_grid_element}">
                    {html_checkbox_comments}</div>
                    <div class="{lookup.html_class_settings_bar_grid_element}">
                    {html_checkbox_values}</div>
                    <div class="{lookup.html_class_settings_bar_grid_element}">
                    {html_checkbox_code}</div>
                    <div class="{lookup.html_class_settings_bar_grid_element}">
                    {html_checkbox_hints}</div>
                    <div class="{lookup.html_class_settings_bar_grid_element}">
                    {html_checkbox_warnings}</div>
                    </div>
                    </div>
                    """

        html_toc = f"""
                <div id="{lookup.html_id_sidebar}">
                <div id="{lookup.html_id_sidebar_wrapper}">
                <div id="{lookup.html_id_sidebar_collapse_button}" 
                onclick="{lookup.js_method_toggle_side_panel}">
                <div id="{lookup.html_id_sidebar_collapse_button_content}">
                </div>
                </div>
                <div id="{lookup.html_id_table_of_contents}">
                
                <ul id="{lookup.html_id_table_of_contents_list}"></ul>
                </div>
                </div>
                </div>
                """

        # get html data of structure
        html_content = f"""
                        <div id={lookup.html_id_content}>
                        {self.structure.get_data().get_html_section()}
                        </div>
                        """

        # header end
        html_end = f"""
                        <script type="text/javascript" src="{lookup.js_file}" ></script>
                        </body>
                        </html>
                        """

        # > > > > > > > > > > > > > > > > > > > >
        # HTML output string concatenation

        html_print = ""

        # header
        html_print += textwrap.dedent(html_header).strip() + "\n"

        # page layout container
        html_print += f'<div id="{lookup.html_id_grid_wrapper}">'

        # settings bar
        html_print += textwrap.dedent(html_settings).strip() + "\n"

        # content
        html_print += html_content + "\n"

        # table of contents
        html_print += textwrap.dedent(html_toc).strip() + "\n"

        # closing tags
        html_print += f'</div>'

        # remove whitespace per line
        html_print += textwrap.dedent(html_end).strip() + "\n"

        # replace placeholders with symbols
        html_print = Converter.insert_symbols(html_print)

        # try writing text to file
        try:
            with open(self.html_file, "w") as f:
                f.write(html_print)
        except:
            # skip rest on fail
            return

        # mark build as successful
        self.build_success = True

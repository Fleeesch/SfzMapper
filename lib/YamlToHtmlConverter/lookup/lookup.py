# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Data-Lookup Module
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..structure.class_entry_code_block import CodeBlock
from ..structure.class_entry_comment_block import CommentBlock
from ..structure.class_entry_example_block import ExampleBlock

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   HTML
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ::: Classes

# Wrapper for a single-line entry
html_class_line_wrapper = "line-wrapper"
html_class_value_only = "value-only"

html_class_section = "section"
html_class_level = "level"
html_class_entry = "entry"
html_class_attribute = "entry-attribute"
html_class_value = "entry-value"
html_class_comment = "comment"
html_class_comment_inline = "comment-inline"
html_class_comment_block = "comment-block"
html_class_code_block = "code-block"
html_class_example_block = "code-block example"
html_class_example_block_header = "example-block-header"
html_class_file_reference = "file-reference"
html_class_settings_checkbox = "settings-checkbox"
html_class_settings_checkbox_label = "settings-checkbox-label"

html_class_symbol_smiley = "symbol-smiley"
html_class_symbol_arrow_left = "symbol-arrow-left"
html_class_symbol_arrow_right = "symbol-arrow-right"
html_class_symbol_arrow_left_right = "symbol-arrow-left-right"
html_class_symbol_arrow_up = "symbol-arrow-up"
html_class_symbol_arrow_down = "symbol-arrow-down"
html_class_symbol_result = "symbol-result"
html_class_settings_bar_grid_element = "settings-bar-element"

# ::: IDs

# Page Layout
html_id_grid_wrapper = "grid-wrapper"  # grid-container
html_id_content = "content"  # entries
html_id_sidebar = "sidebar"  # sidebar (table-of-contents)
html_id_settings_bar = "settings-bar"  # top bar (filter)

# Settings Bar
html_id_settings_bar_grid_container = "settings-bar-wrapper"


# Sidebar Container
html_id_sidebar_wrapper = "sidebar-wrapper"  # grid-container
html_id_sidebar_collapse_button = "sidebar-collapse-button"  # collapse button
html_id_sidebar_collapse_button_content = "sidebar-collapse-button-content"  # collapse button content
html_id_table_of_contents = "table-of-contents"  # table-of-contents container
html_id_table_of_contents_list = "table-of-contents-list"  # list for table-of-contents

# Filter
html_id_filter = "input-filter"  # list for table-of-contents
html_id_filter_wrapper = "input-filter-wrapper"

# Check Boxes
html_id_check_comment_blocks = "input-check-comment-blocks"
html_id_check_comments = "input-check-comments"
html_id_check_values = "input-check-values"
html_id_check_code = "input-check-code"
html_id_check_hints = "input-check-hints"
html_id_check_warnings = "input-check-warnings"

# ::: String Formatting

# use the following syntax:
# {class-name to apply} : [{opening tag}, {closing tag}]
#
# Alternatively, you can leave out to closing tag to spread#
# the formatting to the end of the line

markdown_symbols = {
    ":-)": html_class_symbol_smiley,
    "<-": html_class_symbol_arrow_left,
    "->": html_class_symbol_arrow_right,
    "<->": html_class_symbol_arrow_left_right,
    "^|": html_class_symbol_arrow_up,
    "|^": html_class_symbol_arrow_down,
    "=RESULT=": html_class_symbol_result
}

markdown_blocks = {
    "#--": CommentBlock,
    "#..": CodeBlock,
    "#??": ExampleBlock,
}

markdown = {
    "comment-type": [".t.", ".t."],
    "comment-format": [".f.", ".f."],
    "comment-appendix": ["++"],
    "string-header": [".h."],
    "string-warning": ["!!"],
    "string-hint": ["??"],
    "string-syntax": ["~~", "~~"],
    "string-quote": ['\"\"', '\"\"'],
    "font-bold": ["**", "**"],
    "font-italic": ["//", "//"],
    "font-underline": ["__", "__"],
    "font-strike": ["--", "--"]
}

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#   Javascript
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# File
js_file = "toc.js"

# Methods
js_method_filter_input = "filterInput()"  # apply filter
js_method_toggle_side_panel = "toggleSidePanel()"  # toggle side panel
js_method_copy = "copyLine(event)"  # toggle side panel

js_method_checkbox_change = "checkboxChange(event)"  # toggle side panel


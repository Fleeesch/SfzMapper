# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#   Class : Structure
#
#   Creates and contains YAML-Data converted to a OOP data-structure.
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

from ..file.class_filehandler import FileHandler
from .class_entry import Entry
from .class_entry_comment_block import CommentBlock
from .class_entry_comment import Comment
from .class_entry_file_reference import FileReference
from .class_entry_section import Section
from ..lookup import lookup

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Structure:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, converter):
        from ..class_converter import Converter

        # headers for table of contents
        self.headers: list[str] = []

        # store converter reference
        self.converter: Converter = converter

        # converter file handler
        self.file_handler = self.converter.file_handler

        # entries
        self.entries: list[Entry] = []

        # collect all entries from file
        self.collect_entries_from_file()

        # always create lowest-level section
        self.root_section: Section = Section(self)

        # start constructing the html file
        self.create_structure_from_file(self.root_section)

        # collect headers
        self.collect_headers()

        # format entries
        self.root_section.format_entries()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Create Structure from File
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def create_structure_from_file(self, section: Section):

        # -----------------------------------
        #   Sub-Method : Iterate Section
        # -----------------------------------

        def iterate_section(sec: Section):

            # --- Function : Update BreakCount ---
            def update_breakcount():

                nonlocal break_count

                if entry_next.level < entry_current.level:
                    break_count = abs(entry_current.level - entry_next.level)

            # ---

            # keep track of index
            nonlocal entry_index, break_count, comment_block_make, comment_block

            # go on until break
            while entry_index < len(self.entries):

                if break_count:
                    break_count -= 1
                    break

                # store current entry and next neighbours, based on current index
                entry_current = self.entries[min(max(entry_index, 0), len(self.entries) - 1)]
                entry_next = self.entries[min(entry_index + 1, len(self.entries) - 1)]

                # > > > > > > > > > > > > > > > > > > > >
                #   File Reference

                if entry_current.is_file_reference:
                    sec.add_entry(entry_current)
                    entry_index += 1
                    continue

                # > > > > > > > > > > > > > > > > > > > >
                #   Comment Block Detection

                # check if entry is full line comment
                if entry_current.is_full_line_comment:

                    # declare comment type
                    comment_block_type: CommentBlock | None = None

                    # go through possible comment block types
                    for c_str in lookup.markdown_blocks:

                        # markdown block matches comment string?
                        if c_str in entry_current.line_no_comment:

                            # store comment type from lookup lit
                            comment_block_type = lookup.markdown_blocks[c_str]
                            break

                    # only act of comment type is valid
                    if comment_block_type:

                        # flip comment block making state
                        comment_block_make = not comment_block_make

                        # make comment block if told to do so
                        if comment_block_make:

                            # create block based on looked up type
                            comment_block = comment_block_type(self)

                            # add block to section
                            sec.add_entry(comment_block)

                        # increment index, skip rest
                        entry_index += 1
                        update_breakcount()
                        continue

                #  comment block is being constructed?
                if comment_block_make:

                    # create comment, transfer line
                    comment_new = Comment(self, comment_block)
                    comment_new.set_line(entry_current.line)

                    # add comment to current block
                    comment_block.add_comment(comment_new)

                    # increment index, skip rest
                    entry_index += 1
                    update_breakcount()
                    continue

                # skip full line comments if there's no block
                elif entry_current.is_full_line_comment:
                    entry_index += 1
                    update_breakcount()
                    continue

                # > > > > > > > > > > > > > > > > > > > >
                #   Start of new Section
                if entry_next.level > entry_current.level:

                    # create new section
                    section_new = Section(self)

                    # transfer attributes
                    section_new.set_level(entry_current.level)
                    section_new.set_line(entry_current.line)
                    section_new.set_id_appendix(entry_current.id_appendix)

                    # add new section as entry of current section
                    sec.add_entry(section_new)

                    # increment index
                    entry_index += 1

                    # iterate over created section
                    iterate_section(section_new)

                # > > > > > > > > > > > > > > > > > > > >
                #   Entry / End of Section
                else:

                    # create new entry
                    entry_new = Entry(self)

                    # transfer attributes
                    entry_new.set_level(entry_current.level)
                    entry_new.set_line(entry_current.line)
                    entry_new.set_id_appendix(entry_current.id_appendix)

                    # increment index
                    entry_index += 1

                    # add entry to current section
                    sec.add_entry(entry_new)

                # stop while loop on last section entry
                update_breakcount()

        # reset entry iterating index
        entry_index: int = 0

        # recursion break counter
        break_count: int = 0

        # make comment block
        comment_block: CommentBlock | None = None
        comment_block_make: bool = False

        # iterate through entries as long as entries are available
        while entry_index < len(self.entries):
            iterate_section(section)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add File Reference Entry
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_file_reference_entry(self, file: FileHandler):

        # create reference to file
        file_ref = FileReference(self, file)

        # add to entry list
        self.add_entry(file_ref)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Line to Entry
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def line_to_entry(self, line: str) -> Entry | None:

        # calculate indent
        indent = int((len(line) - len(line.lstrip())) / 2)

        # skip empty line
        if line.strip() == "":
            return None

        # entry creation
        entry = Entry(self)

        # set level
        entry.set_level(indent)

        # set line
        entry.set_line(line)

        # add entry to lookup list
        self.add_entry(entry)

        return entry

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Collect Entries from File
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def collect_entries_from_file(self):

        for f in self.file_handler:

            if len(self.file_handler) > 1:
                self.add_file_reference_entry(f)

            # collect entries
            while f.lines_available():

                # get raw line string
                line = f.get_line_inc()

                # skip yaml header
                if line.strip() == "---":
                    continue

                # skip empty lines
                if not line.strip():
                    continue

                # create entry using line
                entry_new = self.line_to_entry(line)

                # set id appendix for entry
                entry_new.set_id_appendix(f.file_name)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Entry
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def add_entry(self, entry):
        self.entries.append(entry)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get Data
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get_data(self) -> Section:
        return self.root_section

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Collect Headers
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def collect_headers(self):

        # go through root entries, collect headers
        for section in self.root_section.entries:
            self.headers.append(section.id)

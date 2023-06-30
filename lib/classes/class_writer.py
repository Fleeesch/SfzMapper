# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : Writer
#
#   Class that contains a section of a SFZ file
#   so that the file can be written in a
#   non-chronological order
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class Writer:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, instrument, file):

        # builder that uses the writer
        self.instrument = instrument

        # parent file
        self.file = file
        
        # items (section of the content)
        self.items = []

        # content of buffer as a single string
        self.content = ""

        # load symbols
        self.symbols = self.instrument.builder.map_data["symbols"]

        # add writer to instrument writer lookup
        self.file.writers.append(self)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Clear
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def clear(self):
        # reset content
        self.content = ""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Comment
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def comment(self, txt):

        # skip empty data
        if txt is None:
            return

        # create comment
        txt = "// " + txt

        # add comment to buffer
        self.add(txt)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Comment Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def comment_line(self, txt):
        
        # skip empty data
        if txt is None:
            return

        self.comment(self.symbols["comment"]["subline"])

        # create comment
        txt = "// " + txt

        # add comment to buffer
        self.add(txt)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Comment Sub
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def comment_sub(self, txt, level):

        # skip empty data
        if txt is None:
            return

        tabs = ""

        for i in range(0, level):
            tabs += self.symbols["tab"]

        self.line_placeholder()

        # create comment
        txt = "// " + tabs + txt

        # add comment to buffer
        self.add(txt)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Comment Block
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def comment_block(self, txt):

        # skip empty data
        if txt is None:
            return
        
        # optional extra line above first comment line
        self.comment(self.symbols["comment"]["line"])
        self.comment(txt)
        self.comment(self.symbols["comment"]["line"])

        self.line_placeholder()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Comment Large
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def comment_large(self, txt):

        # skip empty data
        if txt is None:
            return

        # optional extra line above first comment line
        self.comment(self.symbols["comment"]["large header"][0])
        self.comment(self.symbols["comment"]["large header"][1])
        self.comment(txt)
        self.comment(self.symbols["comment"]["large header"][1])
        self.comment(self.symbols["comment"]["large header"][0])

        self.line_placeholder()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Header
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def header(self, txt=""):

        # skip empty data
        if txt is None:
            return

        # header formatting
        txt = "<" + txt + ">"

        # add line
        self.line()

        # add to buffer, using a  linebreak
        self.add(txt)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Tag
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def tag(self, tag="", result=""):

        # skip empty data
        if tag is None or result is None:
            return
        
        tag = tag + "=" + str(result)

        # add text
        self.add(tag)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Text
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def text(self, txt=""):

        # skip empty data
        if txt is None:
            return

        # add zexz
        self.add(txt)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    # last statetement used to add content to writer

    def add(self, txt=""):

        # linebreak
        self.line()

        # add to buffer
        self.items.append(Writer.Item(txt))
        
        # first write is done
        self.file.set_first_write(False)

        # raise flag if line is comment
        self.file.set_comment_write("//" in txt)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Space
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def space(self):

        # no whitespace on first write
        if self.file.get_first_write():
            return

        # add space
        self.items.append(Writer.Item(" "))

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    
    def line(self):

        # no whitespace on first write
        if self.file.get_first_write():
            return
        
        # add linebreak
        self.items.append(Writer.Item("\n"))

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Line
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def line_placeholder(self):

        # no whitespace on first write
        if self.file.get_first_write():
            return

        # add linebreak
        self.items.append(Writer.Item("\n" + "//" + self.symbols["line placeholder"]))

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Get
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def get(self):
        
        # assemble the content if required
        if not self.content:
            for item in self.items:
                self.content += item.get()

        # return content
        return self.content

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Subclass : Item
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    class Item:

        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #   Constructor
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

        def __init__(self, content=""):
            
            # store content
            self.content = content

        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
        #   Method : Get
        # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

        def get(self):
            return self.content

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : GUI : Output
#
#   GUI output window for displaying selected process
#   information
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import tkinter as tk

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class GuiOutput:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # default colors
    color_bg = "#1A1A1A"
    color_fg = "#D8D8D8"

    # highlight colors
    color_fg_error = "#DA8080"
    color_fg_success = "#80D080"
    color_fg_remark = "#D0D080"

    # selection coors
    color_select_bg = "#808080"
    color_select_fg = "#FFFFFF"

    # color tags for inline stylization
    COLOR_TAG_NEUTRAL = "color_neutral"
    COLOR_TAG_ERROR = "color_error"
    COLOR_TAG_REMARK = "color_remark"
    COLOR_TAG_SUCCESS = "color_success"

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, gui, row=0, col=0):

        # gui reference
        self.gui = gui

        # gui tkinter reference
        t = self.gui.t

        # text and formatting
        self.text = tk.Text(t, wrap=tk.NONE)
        self.text.grid(row=row, column=col, columnspan=100, sticky=tk.E + tk.W + tk.S + tk.N, **self.gui.padding)

        # color tags
        self.text.tag_config(self.COLOR_TAG_NEUTRAL, foreground=GuiOutput.color_fg)
        self.text.tag_config(self.COLOR_TAG_ERROR, foreground=GuiOutput.color_fg_error)
        self.text.tag_config(self.COLOR_TAG_REMARK, foreground=GuiOutput.color_fg_remark)
        self.text.tag_config(self.COLOR_TAG_SUCCESS, foreground=GuiOutput.color_fg_success)

        # format
        self.text.configure(fg=GuiOutput.color_fg, bg=GuiOutput.color_bg)
        self.text.configure(relief="solid")
        self.text.configure(selectbackground=GuiOutput.color_select_bg)
        self.text.configure(selectforeground=GuiOutput.color_select_fg)

        # lock by default
        self.text.configure(state=tk.DISABLED)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Clear
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def clear(self):

        # unlock
        self.text.configure(state=tk.NORMAL)

        # clear
        self.text.delete('1.0', tk.END)

        # lock
        self.text.configure(state=tk.DISABLED)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Print
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def print(self, msg="", linebreak=False, color_tag=None):

        # unlock
        self.text.configure(state=tk.NORMAL)

        # insert message
        if color_tag:
            self.text.insert(tk.END, msg, color_tag)
        else:
            self.text.insert(tk.END, msg)

        # linebreak
        if linebreak:
            self.text.insert(tk.END, "\n")

        # lock
        self.text.configure(state=tk.DISABLED)

        # scroll to end
        self.text.see(tk.END)

        # refresh gui
        self.gui.refresh()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Print (Neutral) Message
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def print_message(self, msg="", linebreak=False, tag=None):

        self.print(msg, linebreak, tag)

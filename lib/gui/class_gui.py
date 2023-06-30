# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : GUI
#
#   Simple GUI for Sfz Mapper,
#   is created on the spot when the class
#   gets instantiated
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import tkinter as tk

from lib import message
from lib.config import config
from lib.gui.output.class_gui_output import GuiOutput
from lib.gui.path_section.class_gui_path_section import GuiPathSection

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class Gui:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Variables
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # limit of path groups
    path_limit = 10

    # colors : borders
    color_border = "#1C1C1A"

    # colors : window
    color_bg = "#404040"
    color_fg = "#D0D0D0"

    # colors : elements
    color_element_bg = "#101010"
    color_element_fg = "#D5D5D5"

    # colors : pressed elements
    color_element_press_bg = "#606060"
    color_element_press_fg = "#F0F0F0"

    # colors : selected elements
    color_element_select_bg = "#808080"
    color_element_select_fg = "#FFFFFF"

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Method : Format Button
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    @staticmethod
    def format_button(button):
        button.configure(fg=Gui.color_element_fg, bg=Gui.color_element_bg)
        button.configure(relief="solid", overrelief="solid", bd=1)
        button.configure(activebackground=Gui.color_element_press_bg)
        button.configure(activeforeground=Gui.color_element_press_fg)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self):

        # window
        t = tk.Tk()
        self.t = t

        t.iconbitmap("icon.ico")

        # window configuration
        t.title("SFZ Mapper")
        t.geometry("640x480")
        
        t.configure(bg=Gui.color_bg)

        # grid configruation
        t.rowconfigure(0, weight=0)
        t.rowconfigure(1, weight=0)
        t.rowconfigure(21, weight=1)
        t.columnconfigure(1, weight=1)

        # global padding
        self.padding = {"padx": 4, "pady": 4}

        # pathgroup add button
        self.button_add = tk.Button(t, text="Add", width=5)
        self.button_add.grid(row=0, column=0, sticky=tk.S + tk.W, **self.padding)
        self.button_add.configure(command=self.path_add_group)

        # pathgroup delete button
        self.button_del = tk.Button(t, text="Del", width=5)
        self.button_del.grid(row=0, column=1, sticky=tk.S + tk.W, **self.padding)
        self.button_del.configure(command=self.path_remove_group)

        # show settings
        self.button_settings = tk.Button(t, text="Defaults")
        self.button_settings.grid(row=0, column=5, sticky=tk.S + tk.E + tk.W, **self.padding)
        self.button_settings.configure(command=config.show_defaults)

        # show templates
        self.button_templates = tk.Button(t, text="Templates")
        self.button_templates.grid(row=0, column=6, sticky=tk.S + tk.E + tk.W, **self.padding)
        self.button_templates.configure(command=config.show_templates)

        # open home folder
        self.button_source = tk.Button(t, text="Source Folder")
        self.button_source.grid(row=0, column=7, sticky=tk.S + tk.E + tk.W, **self.padding)
        self.button_source.configure(command=config.open_source_folder)

        # separator
        self.separator = tk.Frame(t, bg=Gui.color_border, height=1, bd=0)
        self.separator.grid(row=1, column=0, columnspan=99, sticky=tk.W + tk.E, **self.padding)

        # create path groups
        self.path = []

        # try loading path count
        self.path_count = self.load_path_count()

        # add path groups
        self.path_add_group(self.path_count)

        # output window
        self.output = GuiOutput(self, 21, 0)

        # format buttons
        Gui.format_button(self.button_settings)
        Gui.format_button(self.button_templates)
        Gui.format_button(self.button_source)
        Gui.format_button(self.button_add)
        Gui.format_button(self.button_del)

        # store GUI reference in message
        message.GUI = self

        # show welcome message
        message.welcome_message()

        # closing action
        def on_close():

            # store path data
            self.store_path_count()
            self.store_paths(True)

            # destroy the gui
            t.destroy()

        # register closing action
        t.protocol("WM_DELETE_WINDOW", on_close)

        # main loop
        t.mainloop()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Apply Config
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def update_paths(self):

        # skip if configuration is not available
        if not config.CONFIG_EXT:
            return

        # go through path instances
        for idx, p in enumerate(self.path):

            # get path string
            path_str = config.CONFIG_EXT.get_path(idx)

            # if path string is not empty, set path for group
            if path_str:
                p.set_path(path_str)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Refresh
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def refresh(self):
        # update gui
        self.t.update()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Clear Output
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def clear_output(self):

        self.output.clear()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Add Path Group
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def path_add_group(self, count=1):

        # keep within path limit
        if len(self.path) >= Gui.path_limit:
            return

        # add at least one path
        count = max(count, 1)

        # add given amount of paths
        for i in range(0, count):
            self.path.append(GuiPathSection(self, 4))

        # store the changed path count
        self.store_path_count()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Remove Path Group
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def path_remove_group(self):

        # keep at least one path
        if len(self.path) <= 1:
            return

        # get current pathgroup
        p = self.path[len(self.path) - 1]

        # trigger the removal of all widgets
        p.delete()

        # remove element from list
        self.path.pop()

        # store the changed path count
        self.store_path_count()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Store Paths
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def store_paths(self, no_error_message=False):

        # store all paths in config
        for path in self.path:
            path.store_path_in_config(no_error_message)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Store Path Count
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def store_path_count(self):

        # skip if config doesn't exist
        if not config.CONFIG_EXT:
            return

        # store data
        config.CONFIG_EXT.store_path_count(str(len(self.path)))

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Load Path Count
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def load_path_count(self):

        # skip if config doesn't exist
        if not config.CONFIG_EXT:
            return

        # try loading path count
        try:

            # get data
            return int(config.CONFIG_EXT.get_path_count())

        except:

            # return default path count
            return 1

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Print Message
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def print_message(self, msg="", linebreak=True, tag=None):

        # print message
        self.output.print_message(msg, linebreak, tag)

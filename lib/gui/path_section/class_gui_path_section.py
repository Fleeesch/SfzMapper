# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Class : GUI : Path Section
#
#   Group of GUI elements to be implemented into
#   the GUI for processing a folder tree with
#   the SFZ Mapper
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import tkinter as tk
from os import path
from tkinter import StringVar, filedialog

from lib import message, sfz
from lib.config import config

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Class
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class GuiPathSection:

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Static Varibales
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    # index for calculation positions
    index = 0

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Constructor
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def __init__(self, gui, row_offset=0):

        from lib.gui.class_gui import Gui

        # gui reference
        self.gui = gui
        t = self.gui.t

        # get index
        index = __class__.index
        self.index = index

        # increment index
        __class__.index += 1

        # character string for label indexing
        char_start = ord('A')
        char = chr(char_start + index)

        # label
        name = "Path " + str(char)
        self.label = tk.Label(t, text=name)

        # grid settings
        self.label.grid(row=index + row_offset, column=0, sticky=tk.W, **self.gui.padding)
        self.label.configure(bg=Gui.color_bg, fg=Gui.color_fg)

        # path input field
        self.input = tk.Entry(t)

        self.input.grid(row=index + row_offset, column=1, columnspan=5, sticky=tk.W + tk.E, **self.gui.padding)

        # format input field
        self.input.configure(fg=Gui.color_element_fg, bg=Gui.color_element_bg)
        self.input.configure(relief="solid")
        self.input.configure(selectbackground=Gui.color_element_select_bg)
        self.input.configure(selectforeground=Gui.color_element_select_fg)
        self.input.configure(insertbackground=Gui.color_element_select_fg)

        # folder button
        self.button_open = tk.Button(t, text="Select Folder")
        self.button_open.grid(row=index + row_offset, column=6, sticky=tk.E + tk.W, **self.gui.padding)

        # processing button
        self.button_process = tk.Button(t, text="Process")
        self.button_process.grid(row=index + row_offset, column=7, sticky=tk.E + tk.W, **self.gui.padding)
        
        # format buttons
        Gui.format_button(self.button_open)
        Gui.format_button(self.button_process)

        # store references
        self.input = self.input
        self.path = ""
        self.button_open = self.button_open
        self.button_process = self.button_process

        # event listeners
        self.button_open.configure(command=self.open_folder)
        self.button_process.configure(command=self.process_folder)

        # path input string variable link
        self.path_input_str = StringVar()
        self.input.configure(textvariable=self.path_input_str)

        # try loading path input text
        path = config.CONFIG_EXT.get_path(self.index)

        # add pre filled path
        if path:
            self.input.insert(0, path)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Set Path
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def set_path(self, path_str):

        # check if path is a valid directory
        if path.isdir(path_str):

            # fill input field
            self.input.delete(0, tk.END)
            self.input.insert(0, path_str)

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Open Path
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def open_folder(self):

        # check if path is valid, set it as initial directory
        if path.isdir(self.path_input_str.get()):
            init_dir = self.path_input_str.get()
        else:
            # use c as initial directory
            init_dir = "c:/"

        # folder open dialog
        folder_path = filedialog.askdirectory(initialdir=init_dir)

        # check if chosen path is valid
        if path.isdir(folder_path):
            # set path
            self.set_path(folder_path)
            # store path in external config
            self.store_path_in_config()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Validate Path
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def validate_path(self, path_str):

        if path.isdir(path_str):
            return True
        else:
            return False

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Store Path
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def store_path_in_config(self, no_error_message=False):

        if not self.validate_path(self.path_input_str.get()):

            if not sfz.MAPPING_BUSY:

                # optional error message
                if not no_error_message:
                    message.clear_output()
                    message.error("Path is not valid")

            return False

        # store path in config
        if config.CONFIG_EXT:
            config.CONFIG_EXT.store_path(self.index, self.path_input_str.get())

        # path is valid, return true
        return True

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Process Folder
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def process_folder(self):

        # store path in external config, abort if path is not valid
        if not self.store_path_in_config():
            return

        # make sfz for selected folder tree
        sfz.make_sfz(self.path_input_str.get())

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Delete
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def delete(self):

        # remove widgets
        self.label.destroy()
        self.input.destroy()
        self.button_open.destroy()
        self.button_process.destroy()

        # decrement index
        __class__.index -= 1

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
    #   Method : Process Folder through CLI
    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

    def process_folder_cli(self):

        # store path in external config, abort if path is not valid
        if not self.store_path_in_config():
            return

        # make sfz for selected folder tree
        sfz.make_sfz(self.path_input_str.get())

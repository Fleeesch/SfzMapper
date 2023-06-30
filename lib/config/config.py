# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Config
#
#   Configuration related functions, including
#   the loading and processing of YAML files and
#   the external config file
#
#   Has globals for universal configuration lookup
#   (DEFAULTS, TEMPLATES)
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import copy
import glob
import os
import shutil
from copy import deepcopy
from pathlib import Path

import yaml
from yaml.loader import FullLoader
from deepmerge import Merger

from lib import message, settings
from lib.config.external.class_config_external import ConfigExternal

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Globals
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# source folder
SOURCE_FOLDER = None

# default settings (merged with every map settings)
DEFAULTS = {}

# templates (used globally, gets loaded manually, fused with map file templates)
TEMPLATES = {}

# global templates from template folder
TEMPLATES_GLOBAL = {}

# external config
CONFIG_EXT = None


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Setup External Config
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def setup_external_config():
    global CONFIG_EXT

    # create instance of external config (triggering setup processs)
    CONFIG_EXT = ConfigExternal()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Copy Parts
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def copy_section(source, section_string):
    # ::: Iterate over Parts :::
    def iterate_section(data):

        # go through parts
        for d in data:

            # try getting copy source, skip if nothing found
            try:
                copy_source = data[d]["copy"]
            except:
                continue

            # convert source to list
            if type(copy_source) is not list:
                copy_source = [copy_source]

            # go through sources
            for cs in copy_source:

                try:

                    cs_inst = data[cs]

                    # copy original
                    org = copy.deepcopy(cs_inst)
                    # copy part
                    new = copy.deepcopy(data[d])

                    # merge dicts
                    data[d] = merge_dicts(org, new)

                    # remove copy attribute
                    data[d].pop("copy")

                except:
                    pass

    # ::: Iterate over Data :::

    def iterate_data(data):

        # go through data
        for d in data:

            # check for dict
            if isinstance(data[d], dict):

                # dict is parts
                if d == section_string:
                    # go through parts
                    iterate_section(data[d])
                    # copying done, skip rest
                    return

                # dig deeper into data
                iterate_data(data[d])
                continue

    iterate_data(source)
    # go through data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Apply Snippet Wildcards
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def apply_snippet_wildcards(snippet, arguments):
    # ::: Method : Apply Wildcard to Value :::

    wildcard_symbol = "$"

    def wc_val(data):

        # get position of argument
        d_pos = str(data).find(wildcard_symbol)

        # nothing found? return unchanged value
        if d_pos < 0:
            return data

        # try replacing placeholder with argument value
        try:

            # assume nr is 0
            nr = 0

            try:
                # get number
                nr = data[d_pos + 1]

                # try casting number as int
                nr = int(nr)
            except:
                # >> double digit alternative

                # get number
                nr = str(data[d_pos + 1]) + str(data[d_pos + 2])

                # try casting number as int
                nr = int(nr)

            # create replacement mask
            look_str = wildcard_symbol + str(nr)

            # replace mask with argument value
            val = str(data).replace(look_str, str(arguments[nr - 1]))

            # try casting value as float
            try:
                val = float(val)
                return val
            except:
                # float failed, try casting as int
                try:
                    val = int(val)
                    return val
                except:
                    # int failed, return string
                    val = str(val)
                    return val

        except:
            pass

        # return original data if nothng worked
        return data

    # ::: Method : Iterate through List :::

    def wc_list(data):

        # go through list
        for idx, d in enumerate(data):
            # found another list? dive into it recursively!
            if isinstance(d, list):
                data[idx] = wc_list(data[idx])
                # skip rest
                continue

            # apply wildcard to single argument entry
            data[idx] = wc_val(data[idx])

        # return new list
        return data

    # ::: Method : Iterate through Snippet :::

    def iterate_snippet(data):

        # iterate through snippet
        for d in list(data):

            # entry is list? dive into it!
            if isinstance(data[d], list):
                data[d] = wc_list(data[d])
                # skip rest
                continue

            # entry is a dict? dive into it recursively!
            if isinstance(data[d], dict):
                iterate_snippet(data[d])
                # skip rest
                continue

            # if entry is a single argument object try applying wildcards
            data[d] = wc_val(data[d])

    # remove first argument (contains snippet)
    arguments.pop(0)

    # iterate through snippet
    iterate_snippet(snippet)

    # return changed snippet
    return snippet


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Insert Snippets into DataSet
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def insert_snippets(data_source, tag=""):
    # lookup table for snippet tags
    snippet_lookup = []

    # create lookup table if no tag is given
    if not tag:

        # base snippet
        snippet_lookup.append("snippet")

        # snippet 1 - 10
        for i in range(1, 10):
            snippet_lookup.append("snippet " + str(i))

    else:

        # use tag for lookup
        snippet_lookup.append(tag)

    # lookup for snippets
    global TEMPLATES

    # go through potential snippet tags (or just the one given)
    for snp in snippet_lookup:

        # flag for restarting current for loop
        force_restart = True

        # restart-wrapper
        while force_restart:

            # skip if data is empty
            if not data_source:
                break

            # go through data as list (making it modifiable)
            for d in list(data_source):

                # assume there's no restart required by default
                force_restart = False

                # check if entry is a string with a "snippet" address
                if type(d) is str and d.lower() == snp:

                    # try loading the snippet
                    try:
                        # get snippet data (with and without arguments)
                        if type(data_source[d]) is list:
                            snippet = TEMPLATES["snippet"][data_source[d][0]]

                            # use copy to avoid overwriting
                            snippet = copy.deepcopy(snippet)

                            # arguments available, apply wildcard
                            snippet = apply_snippet_wildcards(snippet, data_source[d])
                        else:
                            # use copy to avoid overwriting
                            snippet = TEMPLATES["snippet"][data_source[d]]

                            # use copy to avoid overwriting
                            snippet = copy.deepcopy(snippet)

                        # transfer snippet content
                        for s in snippet:
                            data_source[s] = snippet[s]

                        # remove original snippet line
                        data_source.pop(d)

                    except:
                        pass

                    # data changed, enable restart and skip rest of the for loop
                    force_restart = True
                    break

                # check if data is a dict
                if isinstance(data_source[d], dict):
                    # iterate recursively over dict
                    insert_snippets(data_source[d], snp)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Fill Placeholders
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def fill_placeholders(builder):
    global TEMPLATES

    placeholder_symbol = "..."

    # path to temporary file
    temp_file = builder.map_path + "/tmp_map.yml"

    # assume there's no placeholder data
    placeholder_data = None

    # try getting a valid placeholder section from templates,
    # skip if there isn't any
    try:
        if TEMPLATES["placeholder"]:
            placeholder_data = TEMPLATES["placeholder"]
        else:
            return None

    except:
        return None

    # create temp file
    shutil.copyfile(builder.map_abs, temp_file)

    # read temp file contents
    with open(temp_file, 'r') as f:
        content = f.read()

    # go through placeholders
    for placeholder in placeholder_data:

        try:
            # convert placeholder data to string
            pl = str(placeholder_data[placeholder])

            # replace placeholder string with value
            content = content.replace(placeholder_symbol + placeholder + placeholder_symbol, pl)
        except:
            continue

    # rewrite temp file with content
    with open(temp_file, 'w') as f:
        content = f.write(content)

    # return created temp file
    return temp_file


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Get : Defaults
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_defaults():
    global DEFAULTS
    return DEFAULTS


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Get : Templates
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def get_templates():
    global TEMPLATES
    return TEMPLATES


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Merge Dictionaries
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def merge_dicts(d1, d2):
    # skip if only one argument is a dict
    # try to return one valid dict
    if type(d1) is not dict:
        if type(d2) is not dict:
            return None
        return d2
    if type(d2) is not dict:
        return d1

    # custom merger: override lists, merge dictionaries
    merger = Merger([
        (list, ["override"]),
        (dict, ["merge"]),
    ],
        ["override"],
        ["override"]
    )

    # create a copy before merging (non-destructive)
    base = deepcopy(d1)
    new = deepcopy(d2)

    # return merged dict
    return merger.merge(base, new)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Merge With Defaults
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def merge_with_defaults(data_in, label):
    global DEFAULTS

    try:
        # merge defaults with input data
        return merge_dicts(DEFAULTS[label], data_in)
    except:
        # return input data if nothing has been found
        return data_in


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load Yaml
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def load_yaml(file=""):
    # skip empty filenames
    if not file:
        return

    # get file name minus extension
    file_split = list(os.path.splitext(file))

    # create file yaml names
    file_yml = file_split[0] + ".yml"
    file_yaml = file_split[0] + ".yaml"

    # init to be returned data array
    data = []

    # file to load
    file_goto = None

    # check if file exists, store address
    if os.path.isfile(file_yml):
        file_goto = file_yml
    elif os.path.isfile(file_yaml):
        file_goto = file_yaml

    # valid file found?
    if file_goto:
        with open(file_goto) as f:

            # load yaml content, store as dict
            data = yaml.load(f, Loader=FullLoader)

    else:
        # no yaml files found, print error message
        message.error("Couldn't load " + file_yml)

    # return the loaded yaml as adict
    return data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load Default Settings
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def load_default_settings():
    global DEFAULTS

    # declare data dict
    data = {}

    # load yaml with default settings (no error output)
    message.progress("+ " + settings.DEFAULTS_NAME + ".yml")

    # load defaults from yaml
    data = load_yaml(settings.DEFAULTS_NAME)

    # no data found? Fatal error, quit everything
    if not data:

        # mark loading as failed
        message.fail()

        # abort software, can't anything without default settings
        message.error_fatal("Couldn't find Default Settings")

    else:
        # sucessfull load
        message.success()

    # store defaults daata
    DEFAULTS = data

    return data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load Local Templates
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def setup_local_templates_from_builder(builder):
    global TEMPLATES, TEMPLATES_GLOBAL

    # clear templates data
    TEMPLATES = {}

    # clear dictionary for merging
    merge_dict = {}

    # try merging global templates with builder template section
    try:
        TEMPLATES = merge_dicts(builder.map_data_global["templates"], TEMPLATES_GLOBAL)
    except:
        # grab data from global templates only
        TEMPLATES = merge_dicts(merge_dict, TEMPLATES_GLOBAL)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load Templates
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def load_templates(extension=""):
    global DEFAULTS, TEMPLATES_GLOBAL

    # create path wildcard for yml and yaml
    pathlists = []
    pathlists.append(Path("./tmp").glob('**/*.yml'))
    pathlists.append(Path("./tmp").glob('**/*.yaml'))

    # declare data dict
    data = {}

    # load hard-coded templates from defaults if available
    if DEFAULTS:
        data = DEFAULTS["templates"]

    # go through template files
    for pathlist in list(pathlists):

        for path in list(pathlist):

            # get file path
            file = str(path)

            # load config
            data_file = load_yaml(file)

            # loading process info
            message.progress("+ " + file)

            # try merging template data with data pool
            try:
                data = merge_dicts(data, data_file)

                # success message
                message.success()
            except:
                # fail mesage
                message.fail()
                pass

    # store and return data
    TEMPLATES_GLOBAL = data
    return data


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Show Defaults
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def show_defaults():
    from lib.YamlToHtmlConverter import YamlToHtmlConverter as yc

    # file to look for
    file_goto = settings.DEFAULTS_NAME + ".yaml"
    file_new = "preview_defaults.html"

    # use yaml to html converter, open file
    yc.yaml_to_html(file_goto, file_new).open_html()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Show Templates
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def show_templates():
    from lib.YamlToHtmlConverter import YamlToHtmlConverter as yc

    # get lookup path list
    pathlists = []
    pathlists.append(Path("./tmp").glob('**/*.yml'))
    pathlists.append(Path("./tmp").glob('**/*.yaml'))

    # list of files to map
    file_list = []

    # go through template files
    for pathlist in list(pathlists):

        for path in list(pathlist):
            # store file path
            file_list.append(os.path.abspath(path))

    # output filename
    file_new = "preview_templates.html"

    # use yaml to html converter, open file
    yc.yaml_to_html(file_list, file_new).open_html()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Store Source Folder
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def store_source_folder():
    global SOURCE_FOLDER

    SOURCE_FOLDER = os.getcwd()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Open Source Folder
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def open_source_folder():
    global SOURCE_FOLDER

    os.startfile(SOURCE_FOLDER)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Remove Temporary Files
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def remove_temp_files(path=None):
    # collect temporary files
    if not path:
        file_list = glob.glob('./*tmp_*')
    else:
        file_list = glob.glob(path + '/*tmp_*')

    # go through files, remove them
    for file in file_list:
        os.remove(file)

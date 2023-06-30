# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# -------------------------------------------------------------------------------
#
#   YamlHtmlConverter v1.0
#
#   Tool for converting a YAML file to an HTML file,
#   turning it into a read-only, browsable manual.
#
# -------------------------------------------------------------------------------
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


from .class_converter import Converter

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Method : Load File
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def yaml_to_html(file: str | list[str], html: str = "out.html") -> Converter | None:
    # try creating a converter, return its instance
    return Converter.create(file, html)



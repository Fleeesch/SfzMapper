# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# ========================================================
#   Module : Documentary
#
#   For creating formatted documentation
#
# ========================================================
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Dependencies
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os

from lib import settings
from lib.config.doc.class_doc_line import DocLine

# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Create HTML from Content
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def content_to_html(input):

    # start with empty content
    content = ""

    # ::: HTML Body :::

    # add html header information
    content += "<html>" + "\n"
    content += "<head>" + "\n"
    content += '<link rel="stylesheet" href="style.css">' + "\n"
    content += "</header>" + "\n"
    content += "<body>" + "\n"

    # cleaned-up input lines
    input_clean = []

    # ::: Remove useless Lines :::

    # block comment mode
    is_block_comment = False

    # for through input lines
    for line in input:

        # convert line to line object, filtering out useless lines in the process
        line_cur = DocLine(line, is_block_comment)

        # flip block comment tag
        if line_cur.block_comment_tag:
            is_block_comment = not is_block_comment

        # mark line as comment if it is one
        if is_block_comment:
            line_cur.block_comment = True

        # skip block comment tags
        if line_cur.block_comment_tag:
            continue

        # skip if line can be ignored and isn't part of a block comment
        if line_cur.ignore and not line_cur.block_comment:
            continue

        # add line to cleaned-up list
        input_clean.append(line_cur)

    # ::: Writing Content :::

    # block comment mode
    is_block_comment = False

    # go through cleaned-up list
    for idx, line in enumerate(input_clean):

        # start and end tags
        tag_start = ""
        tag_end = ""

        line_break = False

        # flags indicating list borders
        first_line = False
        last_line = False

        # mark first line
        if idx == 0:
            first_line = True

        # mark last line
        if idx == len(input_clean) - 1:
            last_line = True

        # get current line
        line_cur = line

        # assume previous and next lines are current line by default
        line_prev = line_cur
        line_next = line_cur

        # try getting previous line
        if not first_line:
            line_prev = input_clean[idx - 1]

        # try getting next line
        if not last_line:
            line_next = input_clean[idx + 1]

        # grab level from previous entry, except for the first line
        if line_cur.block_comment:
            if not first_line:
                line_cur.level = line_prev.level
            else:
                line_cur.level = 0

        # add divider line if required
        if line_prev.level != 0 and line_cur.level == 0:
            tag_start += "<hr>"

        # header indicator
        is_header = False

        # first level is always a header
        if line_cur.level == 0 and not line_cur.block_comment:
            is_header = True
        
        # open block comment group
        if line_cur.block_comment and not line_prev.block_comment:
            tag_start += '<div class="block_comment">'
        
        # start a list if level incremented
        if line_cur.level > line_prev.level:
            tag_start += "<ul>"
        
        # list entry
        if line_cur.level > 0:
            # inline comment
            if line_cur.list_comment:
                # is a header?
                if line_cur.comment_header:
                    tag_start += '<li class="comment_list comment_header">'
                else:
                    # normal inline comment
                    tag_start += '<li class="comment_list">'
            else:
                # conventional line (bullet point)
                tag_start += "<li>"
        
        # comment header opening tag
        if line_cur.comment_header:
            tag_start += '<span class="comment_header">'
        
        # attention header opening tag
        if line_cur.comment_attention:
            tag_start += '<span class="attention">'
        
        # add header tags if line is header
        if is_header:
            tag_start += "<h1># "
            tag_end += "</h1>"
        
        # comment header closing tag
        if line_cur.comment_header:
            tag_end += '</span>'

        # attention header opening tag
        if line_cur.comment_attention:
            tag_end += '</span>'

        # end list point if not header
        if not is_header and line_cur.level > 0:
            tag_end += "</li>"

        # close block comment group
        if line_cur.block_comment and not line_next.block_comment:
            tag_end += '</div>'

        # check if level decremented
        if line_next.level < line_cur.level:

            # calculate key delta
            level_delta = line_cur.level - line_next.level

            # add required amount of list-closing tags
            for i in range(0, level_delta):
                tag_end += "</ul>"

        content += tag_start + line_cur.get() + tag_end + "\n"

        # add comment linebreak
        if line_cur.block_comment:
            content += "<br>"

    # ::: End Tags :::

    content += "</body>" + "\n"
    content += "</html>" + "\n"

    # ::: Return Content :::

    return content


# - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#   Create formatted HTML from YAML
# - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def yaml_to_html(file, output):

    # skip if output file name isn't valid
    if not output:
        return

    # file to look for
    file_goto = None

    # check if defaulsts file exists
    for ext in [".yml", ".yaml"]:

        if os.path.isfile(settings.DEFAULTS_NAME + ext):

            # store default file path
            file_goto = settings.DEFAULTS_NAME + ext
            break

    # file found?
    if file_goto:

        # open file
        with open(file_goto, "r") as f:

            # store lines of file into list
            input = f.read().split("\n")

            # convert content to html
            content = content_to_html(input)

        # write html file
        with open(output, "w", encoding="latin-1") as f:

            f.write(content)

    pass

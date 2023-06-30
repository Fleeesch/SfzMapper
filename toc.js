// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Setup
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

// -------------------------------
//  Globals
// -------------------------------

// CSS selectors
const css_hidden = "hidden";
const css_hidden_overwrite = 'hidden-overwrite';
const css_marked = "marked";
const css_collapsed = "collapsed";
const css_content = "content";
const css_grid_wrapper = "#grid-wrapper";
const css_filter_input = "input-filter";
const css_toc_link = "#table-of-contents a";
const css_section_header_root = '.section.level-0';
const css_linewrapper_root = '.line-wrapper.level-0';
const css_fire_ref = ".file-reference"
const css_attribute = ".entry-attribute";
const css_toc = 'table-of-contents';
const css_toc_list = 'table-of-contents-list';
const css_toc_links = '#table-of-contents-list a';
const css_highlight = 'highlight';
const css_collapse_button = 'sidebar-collapse-button';
const css_collapse_button_content = 'sidebar-collapse-button-content';

const css_checkboxes = 'input[type="checkbox"]';

const css_comment_block = ".comment-block";
const css_comment_inline = ".comment-inline";
const css_value_only = ".value-only";
const css_values = ".entry-value";
const css_code = ".code-block";
const css_warning = ".string-warning";
const css_hint = ".string-hint";

const css_checked = "checked";

const css_id_check_comment_blocks = "input-check-comment-blocks"
const css_id_check_comments = "input-check-comments"
const css_id_check_values = "input-check-values"
const css_id_check_code = "input-check-code"
const css_id_check_hints = "input-check-hints"
const css_id_check_warnings = "input-check-warnings"



// -------------------------------
//  Creating Table of Contents
// -------------------------------

// get table of contents and children
var toc = document.getElementById(css_toc);
var tocList = document.getElementById(css_toc_list);


// get all root level headers
var items = document.querySelectorAll(css_linewrapper_root + ", " + css_fire_ref);

// go through headers
items.forEach(function (item) {
    
    // create list entry with hyperlink
    var listItemLink = document.createElement('a');
    var listItem = document.createElement('li');

    // generate name, implement hyperlink-entry
    listItemLink.textContent = item.textContent.replaceAll(":", "").trim();
    listItemLink.setAttribute("href", "#" + item.id);



    // write html
    listItem.appendChild(listItemLink);
    tocList.appendChild(listItem)

    if (listItemLink.textContent.includes(".yml") || listItemLink.textContent.includes(".yaml")) {
        listItem.classList.add("table-of-contents-file-reference");
    }

});

// -------------------------------
//  Dynamic Scrolling Highlight
// -------------------------------

// collect all the element references
const contentContainer = document.getElementById(css_content);
const contentRootSections = document.querySelectorAll(css_linewrapper_root + ", " + css_fire_ref);
const tocLinks = document.querySelectorAll(css_toc_links)

// create eventlistener for content container scroll events
contentContainer.addEventListener("scroll", () => {

    // get scroll position relative to container
    const scrollPosition = window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;

    // mark the first active entry
    var activeClassSet = false;
    
    // go through entries
    for (const [idx, ct] of contentRootSections.entries()) {
        
        // get bounding box of entry
        elementBox = ct.getBoundingClientRect();
        
        // grab table of contents equivalent
        
        link_last = tocLinks[idx-1];
        link = tocLinks[idx];
        
        // element higher positioned than scroll position or one entry already marked?
        if (elementBox.top - 100 < scrollPosition || activeClassSet) {
            // remove highlight
            link.classList.remove(css_highlight);
        } else {
            // first entry in view!
            
            // add highlight to last link
            link_last.classList.add(css_highlight);
            
            // remove highlight from current link
            link.classList.remove(css_highlight);
            
            // remember marked entry
            activeClassSet = true;
        }

    }

});

// -------------------------------
//  Startup Actions
// -------------------------------

// apply filter
filterInput()

// update display elements
updateCheckboxes()

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Toggle Side Panel
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function toggleSidePanel() {

    sidepanel = document.querySelector(css_grid_wrapper);

    if (!sidepanel) return;

    if (sidepanel.classList.contains(css_collapsed)) {
        sidepanel.classList.remove(css_collapsed);
    } else {
        sidepanel.classList.add(css_collapsed);
    }



}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Line to Clipboard
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

// element marked for being copied
var previouslyMarkedElement = null;

function copyLine(event) {

    // get clicked element
    var clickedElement = event.currentTarget;

    // filter text to copy
    var textToCopy = clickedElement.textContent.trim().split(":")[0] + ":";

    // copy to clipboard
    navigator.clipboard.writeText(textToCopy)

    // remove previous marker (if available)
    if (previouslyMarkedElement) {
        previouslyMarkedElement.classList.remove(css_marked);
    }

    // add marker
    clickedElement.classList.add(css_marked);

    // store marked element
    previouslyMarkedElement = clickedElement;

}


// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Filter Structure Elements
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function filterStructureElements(filter) {

    // get root headers
    lines = document.querySelectorAll(css_section_header_root);

    // iterate over root headers
    lines.forEach(function iterate(line) {

        // get child attribute
        children = line.querySelectorAll(css_attribute);

        // get formatted text of attribute
        var text = children[0].textContent.trim();

        // skip file references
        if (text.includes(".yaml") || text.includes(".yml")) {
            return;
        }

        // hide containers that don't match filters
        if (text.includes(filter)) {
            line.classList.remove(css_hidden);
        } else {
            line.classList.add(css_hidden);
        }

    });


}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Filter Table of Contents
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function filterTableOfContents(filter) {

    // get hyperlinks from table of contents
    lines = document.querySelectorAll(css_toc_link);

    // iterate over lines
    lines.forEach(function iterate(link, index) {

        // store formatted line
        var text = link.textContent.trim();

        // skip file references
        if (text.includes(".yaml") || text.includes(".yml")) {
            return;
        }


        // remove lines that don't match filter
        if (text.includes(filter)) {
            link.classList.remove(css_hidden);
        } else {
            link.classList.add(css_hidden);
        }

    });



}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Filter Input
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function filterInput() {


    // get formatted input text
    input = document.getElementById(css_filter_input).value.trim();

    // filter structure
    filterStructureElements(input);

    // filter table of contents
    filterTableOfContents(input);

}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Update Checkboxes
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function updateCheckboxes() {

    elements = document.querySelectorAll(css_checkboxes);

    for (const [idx, e] of elements.entries()) {

        updateCheckbox(e)

    }

}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Function : Update Checkboxe
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function updateCheckbox(element) {

    function showHideElements(selector, hide) {

        elements = document.querySelectorAll(selector);

        for (const [idx, e] of elements.entries()) {

            if (hide) {
                e.classList.add(css_hidden_overwrite);
            } else {
                e.classList.remove(css_hidden_overwrite);
            }

        }

    }

    checkState = element.checked;

    if (element.id === css_id_check_comment_blocks) {
        showHideElements(css_comment_block, !checkState);
    }

    if (element.id === css_id_check_comments) {
        showHideElements(css_comment_inline, !checkState);
    }

    if (element.id === css_id_check_values) {
        showHideElements(css_values, !checkState);
        showHideElements(css_value_only, !checkState);
    }

    if (element.id === css_id_check_code) {
        showHideElements(css_code, !checkState);
    }

    if (element.id === css_id_check_hints) {
        showHideElements(css_hint, !checkState);
    }

    if (element.id === css_id_check_warnings) {
        showHideElements(css_warning, !checkState);
    }

}

// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//  Event : Checkbox Change
// - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

function checkboxChange(event) {

    var element = event.currentTarget;

    updateCheckbox(element);


}


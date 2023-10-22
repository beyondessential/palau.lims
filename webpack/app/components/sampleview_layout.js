/* Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c sampleview_layout.coffee
*/
var SampleViewLayoutController;

/*
This controller makes possible to collapse and expand sections from sample view
and keep the configuration stored in a cookie. This prevents the user to have to
constantly scroll as they enter and verify results.
https://github.com/beyondessential/png.lims/issues/163
*/
SampleViewLayoutController = class SampleViewLayoutController {
  constructor() {
    var j, len, section, sections;
    /*
    Returns whether this controller needs to be loaded or not
    */
    this.is_required = this.is_required.bind(this);
    /*
    Event triggered when a toggle selector is clicked. Toggles the visibility of
    the section associated to the toggle selector and stores the visibility into
    a cookie
    */
    this.on_toggle_selector_clicked = this.on_toggle_selector_clicked.bind(this);
    /*
    Initializes a toggle selector
    */
    this.init_toggle = this.init_toggle.bind(this);
    /*
    Sets the visibility of sample sections based on the configuration stored in
    cookies
    */
    this.init_sections_visibility = this.init_sections_visibility.bind(this);
    /*
    Prints a debug message in console with this component name prefixed
    */
    this.debug = this.debug.bind(this);
    // Do not load this controller unless required
    if (!this.is_required()) {
      return;
    }
    this.debug("load");
    // List of [anchor_selector, section_selector, section_id]
    sections = [["#content h1", "#senaite-sampleheader", "palau-lims-sample-header"], ["#content h1", "div[id=ar-attachments]", "palau-lims-sample-header"], ["div.remarks-widget h3", "div.remarks-widget div", "palau-lims-sample-remarks-section"], ["div.analysis-listing-table h3", "div.analysis-listing-table form", "palau-lims-sample-analyses-section"], ["div[id=results-interpretation] h3", "div[id=results-interpretation] form", "palau-lims-sample-results-interpretation-section"]];
// Initializes toggle sections
    for (j = 0, len = sections.length; j < len; j++) {
      section = sections[j];
      this.init_toggle(section[0], section[1], section[2]);
    }
    // Bind the event handler to the elements
    $("body").on("click", ".toggle_selector", this.on_toggle_selector_clicked);
    // Show/Hide sections depending on the cookie value(s)
    this.init_sections_visibility();
    return this;
  }

  is_required() {
    var clazz, i, j, len, ref, targets;
    targets = ["portaltype-analysisrequest"];
    ref = document.body.classList;
    for (i = j = 0, len = ref.length; j < len; i = ++j) {
      clazz = ref[i];
      if (targets.includes(clazz)) {
        return true;
      }
    }
    return false;
  }

  on_toggle_selector_clicked(event) {
    var el, j, len, section, section_id, sections, visible;
    this.debug("on_toggle_selector_clicked");
    el = event.currentTarget;
    section_id = el.getAttribute("target-section");
    sections = document.querySelectorAll(`[section=${section_id}]`);
    for (j = 0, len = sections.length; j < len; j++) {
      section = sections[j];
      if (!section) {
        continue;
      }
      visible = this.is_visible(section);
      if (visible) {
        $(section).hide();
      } else {
        $(section).show();
      }
    }
    return site.set_cookie(section_id, !visible);
  }

  init_toggle(anchor_selector, section_selector, section_id) {
    var anchor, section;
    this.debug(`init_toggle:anchor_selector='${anchor_selector}',section_selector='${section_selector}',section_id='${section_id}'`);
    anchor = document.querySelector(anchor_selector);
    if (!anchor) {
      return;
    }
    anchor.classList.add("toggle_selector");
    anchor.setAttribute("target-section", section_id);
    section = document.querySelector(section_selector);
    if (!section) {
      return;
    }
    return section.setAttribute("section", section_id);
  }

  /*
  Returns whether the element is visible or not
  */
  is_visible(element) {
    if ($(element).css("display") === "none") {
      return false;
    }
    return true;
  }

  init_sections_visibility() {
    var anchor, anchors, j, len, results, section, section_id, sections, selector, visible;
    this.debug("set_visibility");
    selector = ".toggle_selector";
    anchors = document.querySelectorAll(".toggle_selector");
    results = [];
    for (j = 0, len = anchors.length; j < len; j++) {
      anchor = anchors[j];
      section_id = anchor.getAttribute("target-section");
      visible = site.read_cookie(section_id) || "true";
      this.debug(`section_id=${section_id}, visible=${visible}`);
      visible = visible === "true";
      sections = document.querySelectorAll(`[section=${section_id}]`);
      results.push((function() {
        var k, len1, results1;
        results1 = [];
        for (k = 0, len1 = sections.length; k < len1; k++) {
          section = sections[k];
          if (visible) {
            results1.push($(section).show());
          } else {
            results1.push($(section).hide());
          }
        }
        return results1;
      })());
    }
    return results;
  }

  debug(message) {
    return console.debug("[palau.lims]", "SampleViewLayoutController::" + message);
  }

};

export default SampleViewLayoutController;


/* Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c sampleview_layout.coffee
 */

/*
This controller makes possible to collapse and expand sections from sample view
and keep the configuration stored in a cookie. This prevents the user to have to
constantly scroll as they enter and verify results.
https://github.com/beyondessential/pnghealth.lims/issues/163
 */
var SampleViewLayoutController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

SampleViewLayoutController = (function() {
  function SampleViewLayoutController() {
    this.debug = bind(this.debug, this);
    this.init_sections_visibility = bind(this.init_sections_visibility, this);
    this.init_toggle = bind(this.init_toggle, this);
    this.on_toggle_selector_clicked = bind(this.on_toggle_selector_clicked, this);
    this.is_required = bind(this.is_required, this);
    var j, len, section, sections;
    if (!this.is_required()) {
      return;
    }
    this.debug("load");
    sections = [["#content h1", "#senaite-sampleheader", "png-lims-sample-header"], ["#content h1", "div[id=ar-attachments]", "png-lims-sample-header"], ["div.remarks-widget h3", "div.remarks-widget div", "png-lims-sample-remarks-section"], ["div.analysis-listing-table h3", "div.analysis-listing-table form", "png-lims-sample-analyses-section"], ["div[id=results-interpretation] h3", "div[id=results-interpretation] form", "png-lims-sample-results-interpretation-section"]];
    for (j = 0, len = sections.length; j < len; j++) {
      section = sections[j];
      this.init_toggle(section[0], section[1], section[2]);
    }
    $("body").on("click", ".toggle_selector", this.on_toggle_selector_clicked);
    this.init_sections_visibility();
    return this;
  }


  /*
  Returns whether this controller needs to be loaded or not
   */

  SampleViewLayoutController.prototype.is_required = function() {
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
  };


  /*
  Event triggered when a toggle selector is clicked. Toggles the visibility of
  the section associated to the toggle selector and stores the visibility into
  a cookie
   */

  SampleViewLayoutController.prototype.on_toggle_selector_clicked = function(event) {
    var el, j, len, section, section_id, sections, visible;
    this.debug("on_toggle_selector_clicked");
    el = event.currentTarget;
    section_id = el.getAttribute("target-section");
    sections = document.querySelectorAll("[section=" + section_id + "]");
    for (j = 0, len = sections.length; j < len; j++) {
      section = sections[j];
      visible = this.is_visible(section);
      if (visible) {
        $(section).hide();
      } else {
        $(section).show();
      }
    }
    return site.set_cookie(section_id, !visible);
  };


  /*
  Initializes a toggle selector
   */

  SampleViewLayoutController.prototype.init_toggle = function(anchor_selector, section_selector, section_id) {
    var anchor, section;
    this.debug("init_toggle:anchor_selector='" + anchor_selector + "',section_selector='" + section_selector + "',section_id='" + section_id + "'");
    anchor = document.querySelector(anchor_selector);
    anchor.classList.add("toggle_selector");
    anchor.setAttribute("target-section", section_id);
    section = document.querySelector(section_selector);
    return section.setAttribute("section", section_id);
  };


  /*
  Returns whether the element is visible or not
   */

  SampleViewLayoutController.prototype.is_visible = function(element) {
    if ($(element).css("display") === "none") {
      return false;
    }
    return true;
  };


  /*
  Sets the visibility of sample sections based on the configuration stored in
  cookies
   */

  SampleViewLayoutController.prototype.init_sections_visibility = function() {
    var anchor, anchors, j, len, results, section, section_id, sections, selector, visible;
    this.debug("set_visibility");
    selector = ".toggle_selector";
    anchors = document.querySelectorAll(".toggle_selector");
    results = [];
    for (j = 0, len = anchors.length; j < len; j++) {
      anchor = anchors[j];
      section_id = anchor.getAttribute("target-section");
      visible = site.read_cookie(section_id) || "true";
      this.debug("section_id=" + section_id + ", visible=" + visible);
      visible = visible === "true";
      sections = document.querySelectorAll("[section=" + section_id + "]");
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
  };


  /*
  Prints a debug message in console with this component name prefixed
   */

  SampleViewLayoutController.prototype.debug = function(message) {
    return console.debug("[palau.lims]", "SampleViewLayoutController::" + message);
  };

  return SampleViewLayoutController;

})();

export default SampleViewLayoutController;

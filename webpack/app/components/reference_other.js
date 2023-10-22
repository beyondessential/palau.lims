/* Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c reference_other.coffee
*/
var ReferenceOtherController;

/*
This controller is in charge of handling the behavior of ReferenceOtherWidget
*/
ReferenceOtherController = class ReferenceOtherController {
  constructor() {
    var el, j, len, ref;
    /*
    Returns whether this controller needs to be loaded or not
    */
    this.is_required = this.is_required.bind(this);
    /*
    Binds callbacks on elements
    Attaches all the events to the body and refine the selector to delegate the
    event: https://learn.jquery.com/events/event-delegation/
    */
    this.bind_event_handler = this.bind_event_handler.bind(this);
    /*
    Event triggered when the checkbox 'Other' is selected
    */
    this.on_reference_other_selector_change = this.on_reference_other_selector_change.bind(this);
    /*
    Event triggered when a reference is selected
    */
    this.on_reference_selected = this.on_reference_selected.bind(this);
    /*
    Event triggered when areference is deselected
    */
    this.on_reference_deselected = this.on_reference_deselected.bind(this);
    // Do no load this controller unless required
    //return unless @is_required()
    this.reference_other_selector = "input.reference-otherfield-check";
    this.reference_value_selector = "div.palau-referenceother-widget-input";
    // Bind the event handler to the elements
    this.bind_event_handler();
    ref = document.querySelectorAll(this.reference_other_selector);
    for (j = 0, len = ref.length; j < len; j++) {
      el = ref[j];
      // hide/show all "Other" fields from ReferenceOtherWidget
      $(el).trigger("change");
    }
    return this;
  }

  is_required() {
    var clazz, i, j, len, ref, targets;
    targets = ["template-ar_add", "portaltype-analysisrequest"];
    ref = document.body.classList;
    for (i = j = 0, len = ref.length; j < len; i = ++j) {
      clazz = ref[i];
      if (targets.includes(clazz)) {
        return true;
      }
    }
    return false;
  }

  bind_event_handler() {
    $("body").on("change", this.reference_other_selector, this.on_reference_other_selector_change);
    $("body").on("select", this.reference_value_selector, this.on_reference_selected);
    return $("body").on("deselect", this.reference_value_selector, this.on_reference_deselected);
  }

  on_reference_other_selector_change(event) {
    var el, target, target_id;
    el = event.currentTarget;
    target_id = $(el).attr("data_target");
    target = document.querySelector("#" + target_id);
    if (el.checked) {
      return $(target).show();
    } else {
      $(target).hide();
      return $(target).val("");
    }
  }

  on_reference_selected(event) {
    var el, target, target_id;
    el = event.currentTarget;
    target_id = "textarea#" + $(el).attr("id") + "_other";
    target = document.querySelector(target_id);
    $(target).hide();
    return $(target).val("");
  }

  on_reference_deselected(event) {
    var el, target, target_id;
    el = event.currentTarget;
    target_id = "textarea#" + $(el).attr("id") + "_other";
    target = document.querySelector(target_id);
    return $(target).show();
  }

};

export default ReferenceOtherController;

/* Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c reference_other.coffee
*/
var ReferenceOtherController;

/*
This controller is in charge of handling the behavior of ReferenceOtherWidget
*/
ReferenceOtherController = class ReferenceOtherController {
  constructor() {
    var el, field_name, i, len, ref;
    /*
    Binds callbacks on elements
    Attaches all the events to the body and refine the selector to delegate the
    event: https://learn.jquery.com/events/event-delegation/
    */
    this.bind_event_handler = this.bind_event_handler.bind(this);
    /*
    Returns a list of fieldnames with a reference widget bound
    */
    this.get_field_names = this.get_field_names.bind(this);
    /*
    Returns the HTML element where other is rendered
    */
    this.get_other_reference_element = this.get_other_reference_element.bind(this);
    /*
    Returns the HTML element where the search input is rendered
    */
    this.get_search_reference_element = this.get_search_reference_element.bind(this);
    /*
    Returns the HTML element with the other text
    */
    this.get_other_check_element = this.get_other_check_element.bind(this);
    /*
    Returns the HTML element with the other text
    */
    this.get_other_text_element = this.get_other_text_element.bind(this);
    this.has_references = this.has_references.bind(this);
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
    this.reference_other_selector = "input.reference-otherfield-check";
    this.reference_value_selector = "div.palau-referenceother-widget-input";
    // Bind the event handler to the elements
    this.bind_event_handler();
    ref = this.get_field_names();
    // hide/show all "Other" fields from ReferenceOtherWidget
    for (i = 0, len = ref.length; i < len; i++) {
      field_name = ref[i];
      if (this.has_references(field_name)) {
        el = this.get_other_reference_element(field_name);
        el.hide();
      } else {
        el = this.get_other_check_element(field_name);
        $(el).trigger("change");
      }
    }
    return this;
  }

  bind_event_handler() {
    $("body").on("change", this.reference_other_selector, this.on_reference_other_selector_change);
    $("body").on("select", this.reference_value_selector, this.on_reference_selected);
    return $("body").on("deselect", this.reference_value_selector, this.on_reference_deselected);
  }

  get_field_names() {
    var element, elements, field_names, i, len;
    field_names = [];
    elements = document.querySelectorAll(this.reference_value_selector);
    for (i = 0, len = elements.length; i < len; i++) {
      element = elements[i];
      field_names.push($(element).attr("id"));
    }
    return field_names;
  }

  get_other_reference_element(field_name) {
    var el, selector;
    selector = "#" + field_name + "_other_field";
    el = document.querySelector(selector);
    return $(el);
  }

  get_search_reference_element(field_name) {
    var el, selector;
    selector = "div.uidreferencefield[id='" + field_name + "']";
    el = document.querySelector(selector);
    return $(el);
  }

  get_other_check_element(field_name) {
    var el, selector;
    selector = "#" + field_name + "_checkbox";
    el = document.querySelector(selector);
    return $(el);
  }

  get_other_text_element(field_name) {
    var el, selector;
    selector = "#" + field_name + "_other";
    el = document.querySelector(selector);
    return $(el);
  }

  has_references(field_name) {
    var el, selector;
    selector = `textarea[name='${field_name}'].queryselectwidget-value`;
    el = document.querySelector(selector);
    if (!el) {
      return;
    }
    if ($(el).val()) {
      return true;
    }
    return false;
  }

  on_reference_other_selector_change(event) {
    var el, field_name, other, search;
    el = event.currentTarget;
    field_name = $(el).attr("data_field");
    other = this.get_other_text_element(field_name);
    search = this.get_search_reference_element(field_name);
    if (el.checked) {
      // display the text box for manual entry
      other.show();
      // hide the reference widget selector
      return search.hide();
    } else {
      // hide the text box for manual entry
      other.hide();
      other.val("");
      // display the reference widget selector
      return search.show();
    }
  }

  on_reference_selected(event) {
    var el, field_name, other, other_checkbox;
    el = event.currentTarget;
    field_name = $(el).attr("id");
    // Uncheck and hide the "Other" checkbox
    other_checkbox = this.get_other_check_element(field_name);
    other_checkbox.checked = false;
    other = this.get_other_reference_element(field_name);
    return other.hide();
  }

  on_reference_deselected(event) {
    var el, field_name, other;
    el = event.currentTarget;
    field_name = $(el).attr("id");
    // Show the "Other" checkbox
    other = this.get_other_reference_element(field_name);
    return other.show();
  }

};

export default ReferenceOtherController;

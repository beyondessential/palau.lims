
/* Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c referenceother.coffee
 */

/*
This controller is in charge of handling the behavior of UIDReferenceOtherFields
 */
var ReferenceOtherController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

ReferenceOtherController = (function() {
  function ReferenceOtherController() {
    this.on_reference_other_selector_change = bind(this.on_reference_other_selector_change, this);
    this.bind_event_handler = bind(this.bind_event_handler, this);
    this.is_required = bind(this.is_required, this);
    var el, j, len, ref;
    if (!this.is_required()) {
      return;
    }
    this.reference_other_selector = "input.reference-otherfield-check";
    this.bind_event_handler();
    ref = document.querySelectorAll(this.reference_other_selector);
    for (j = 0, len = ref.length; j < len; j++) {
      el = ref[j];
      $(el).trigger("change");
    }
    return this;
  }


  /*
  Returns whether this controller needs to be loaded or not
   */

  ReferenceOtherController.prototype.is_required = function() {
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
  };


  /*
  Binds callbacks on elements
  Attaches all the events to the body and refine the selector to delegate the
  event: https://learn.jquery.com/events/event-delegation/
   */

  ReferenceOtherController.prototype.bind_event_handler = function() {
    return $("body").on("change", this.reference_other_selector, this.on_reference_other_selector_change);
  };


  /*
  Event triggered when the checkbox 'Other' is selected
   */

  ReferenceOtherController.prototype.on_reference_other_selector_change = function(event) {
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
  };

  return ReferenceOtherController;

})();

export default ReferenceOtherController;

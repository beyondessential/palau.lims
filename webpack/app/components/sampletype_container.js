
/* Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c sampletype_container.coffee
 */

/*
This controller is in charge of displaying the suitable widget/control for
container selection depending on the selected sample type.
Sample Type content type has the field "ContainerWidget" that allows the user to
define the control to display in Add sample form or sample view depending on the
sample type selected.
If the selected Sample Type has the widget "bottles" selected, the system hides
the "Container" field from the form and displays "Bottles" field instead.
https://github.com/beyondessential/pnghealth.lims/issues/28
 */
var SampleTypeContainerController,
  bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
  indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

SampleTypeContainerController = (function() {
  function SampleTypeContainerController() {
    this.debug = bind(this.debug, this);
    this.get_portal_url = bind(this.get_portal_url, this);
    this.ajax_submit = bind(this.ajax_submit, this);
    this.fetch = bind(this.fetch, this);
    this.set_visible = bind(this.set_visible, this);
    this.round = bind(this.round, this);
    this.get_float_value = bind(this.get_float_value, this);
    this.calculate_volume = bind(this.calculate_volume, this);
    this.set_volume_readonly = bind(this.set_volume_readonly, this);
    this.toggle_container_visibility = bind(this.toggle_container_visibility, this);
    this.update_container = bind(this.update_container, this);
    this.get_sample_index = bind(this.get_sample_index, this);
    this.on_sample_type_selected = bind(this.on_sample_type_selected, this);
    this.on_bottle_container_blur = bind(this.on_bottle_container_blur, this);
    this.on_bottle_weight_change = bind(this.on_bottle_weight_change, this);
    this.on_template_selected = bind(this.on_template_selected, this);
    this.bind_event_handler = bind(this.bind_event_handler, this);
    this.is_required = bind(this.is_required, this);
    var bottles, el, j, len, ref;
    if (!this.is_required()) {
      return;
    }
    this.debug("load");
    this.sample_type_selector = "input[id^='SampleType']";
    this.template_selector = "input[id^='Template']";
    this.bottle_weights_selector = "input[id^='Bottles-'][id*='-Weight-']";
    this.bottle_containers_selector = "input[id^='Bottles-'][id*='-Container-']";
    this.bind_event_handler();
    if (indexOf.call(document.body.classList, "template-ar_add") >= 0) {
      ref = document.querySelectorAll(this.sample_type_selector);
      for (j = 0, len = ref.length; j < len; j++) {
        el = ref[j];
        $(el).trigger("selected");
      }
    } else {
      bottles = document.querySelector("div[data-fieldname='Bottles']");
      if (bottles) {
        el = document.querySelector("input[id='Volume']");
        el.setAttribute("readonly", "readonly");
      }
    }
    return this;
  }


  /*
  Returns whether this controller needs to be loaded or not
   */

  SampleTypeContainerController.prototype.is_required = function() {
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

  SampleTypeContainerController.prototype.bind_event_handler = function() {
    this.debug("bind_event_handler");
    $("body").on("selected", this.sample_type_selector, this.on_sample_type_selected);
    $("body").on("selected", this.template_selector, this.on_template_selected);
    $("body").on("blur", this.bottle_containers_selector, this.on_bottle_container_blur);
    return $("body").on("change", this.bottle_weights_selector, this.on_bottle_weight_change);
  };


  /*
  Event triggered when the value for Sample Template field changes
  Checks for the selection control widget assigned to the Sample Type the
  selected Template is assigned to and hides/display other fields (Bottles,
  Container) accordingly.
   */

  SampleTypeContainerController.prototype.on_template_selected = function(event) {
    var el, idx, uid;
    this.debug("on_template_selected");
    el = event.currentTarget;
    idx = this.get_sample_index(el);
    uid = $("#" + el.id).attr("uid");
    if (!uid) {
      return;
    }
    return this.fetch(uid, []).done(function(data) {
      var sample_type_uid;
      if (data) {
        sample_type_uid = data["SampleType_uid"];
        return this.update_container(idx, sample_type_uid);
      }
    });
  };


  /*
  Event triggered when the weight value of a record from inside the Bottles
  widget is changed. Calculates the sample volume of each bottle as the
  difference between the weight set and the bottle's dry weight
   */

  SampleTypeContainerController.prototype.on_bottle_weight_change = function(event) {
    var el, sample_idx;
    this.debug("on_bottle_weight_change");
    el = event.currentTarget;
    sample_idx = this.get_sample_index(el);
    return this.calculate_volume(sample_idx);
  };


  /*
  Event triggered when the container value of a record from inside the Bottles
  widget changes. Calculates the sample volume of each bottle as the difference
  between the weight set and the bottle's dry weight
   */

  SampleTypeContainerController.prototype.on_bottle_container_blur = function(event) {
    var el, sample_idx;
    this.debug("on_bottle_container_blur");
    el = event.currentTarget;
    sample_idx = this.get_sample_index(el);
    return this.calculate_volume(sample_idx);
  };


  /*
  Event triggered when the value for Sample Type field changes.
  Checks for the selection control widget assigned to the Sample Type and
  hides/display other fields (Bottles, Container) in accordance
   */

  SampleTypeContainerController.prototype.on_sample_type_selected = function(event) {
    var el, idx, uid;
    this.debug("on_sample_type_selected");
    el = event.currentTarget;
    idx = this.get_sample_index(el);
    uid = $("#" + el.id).attr("uid");
    return this.update_container(idx, uid);
  };


  /*
  Returns the column/sample index of the Add form for the element passed in
   */

  SampleTypeContainerController.prototype.get_sample_index = function(element) {
    var parent;
    this.debug("get_sample_index:element=" + element.id);
    parent = element.closest("td[arnum]");
    if (!parent) {
      return null;
    }
    return $(parent).attr("arnum");
  };


  /*
  Updates the type of widget to display as container (traditional Container or
  Bottles) depending on the values set for Sample Type and/or Sample Template
   */

  SampleTypeContainerController.prototype.update_container = function(sample_index, sample_type_uid) {
    var field_name;
    this.debug("update_container:sample_index=" + sample_index + ",sample_type_uid=" + sample_type_uid);
    if (!sample_type_uid) {
      this.toggle_container_visibility(sample_index, true);
      return this.set_volume_readonly(sample_index, false);
    } else {
      field_name = "ContainerWidget";
      return this.fetch(sample_type_uid, field_name).done(function(data) {
        var show_container;
        show_container = false;
        if (data) {
          show_container = data[field_name] === "container";
        }
        this.toggle_container_visibility(sample_index, show_container);
        this.set_volume_readonly(sample_index, !show_container);
        if (!show_container) {
          return this.calculate_volume(sample_index);
        }
      });
    }
  };


  /*
  Sets the visibility of both the "Container" field and the "Bottles" field
  Displays the "Container" and hides the "Bottles" if true
   */

  SampleTypeContainerController.prototype.toggle_container_visibility = function(sample_index, show_container) {
    this.debug("toggle_container_visibility:sample_index=" + sample_index + ",show_container=" + show_container);
    this.set_visible("Container", sample_index, show_container);
    return this.set_visible("Bottles", sample_index, !show_container);
  };


  /*
  Sets the readonly mode of the Volume field
   */

  SampleTypeContainerController.prototype.set_volume_readonly = function(sample_index, readonly) {
    var el, selector;
    this.debug("set_volume_readonly:sample_index=" + sample_index + ",readonly=" + readonly);
    selector = "#Volume";
    if (sample_index) {
      selector = "#Volume-" + sample_index;
    }
    el = document.querySelector(selector);
    if (readonly) {
      return el.setAttribute("readonly", "readonly");
    } else {
      return el.removeAttribute("readonly");
    }
  };


  /*
  Calculates the volumes of each bottle and the total volume of the sample
   */

  SampleTypeContainerController.prototype.calculate_volume = function(sample_index) {
    var elements, selector, that, total_volume, volume, volume_selector;
    this.debug("calculate_volume:sample_index=" + sample_index);
    total_volume = 0;
    selector = "tr.records_row_Bottles";
    if (sample_index) {
      selector = "tr.records_row_Bottles-" + sample_index;
    }
    elements = document.querySelectorAll(selector);
    that = this;
    $.each(elements, function(index, el) {
      var dry_weight, dry_weight_selector, vol, volume, volume_selector, weight, weight_selector;
      weight_selector = "#Bottles-Weight-" + index;
      if (sample_index) {
        weight_selector = "#Bottles-" + sample_index + "-Weight-" + index;
      }
      weight = el.querySelector(weight_selector);
      weight = that.get_float_value(weight);
      that.debug("Not a valid volume: " + weight);
      dry_weight_selector = "#Bottles-DryWeight-" + index;
      if (sample_index) {
        dry_weight_selector = "#Bottles-" + sample_index + "-DryWeight-" + index;
      }
      dry_weight = el.querySelector(dry_weight_selector);
      dry_weight = that.get_float_value(dry_weight);
      that.debug("Not a valid volume: " + dry_weight);
      vol = weight - dry_weight;
      if (vol <= 0) {
        that.debug("Not a valid bottle volume: " + vol);
        vol = "";
      } else {
        vol = that.round(vol * 1.05, 3);
        total_volume = total_volume + vol;
      }
      volume_selector = "#Bottles-Volume-" + index;
      if (sample_index) {
        volume_selector = "#Bottles-" + sample_index + "-Volume-" + index;
      }
      volume = el.querySelector(volume_selector);
      return volume.value = vol;
    });
    total_volume = parseFloat(total_volume);
    total_volume = this.round(total_volume, 4);
    if (total_volume <= 0) {
      this.debug("Not a valid volume: " + total_volume);
      total_volume = "";
    } else {
      total_volume += " ml";
    }
    volume_selector = "#Volume";
    if (sample_index) {
      volume_selector = "#Volume-" + sample_index;
    }
    volume = document.querySelector(volume_selector);
    return volume.value = total_volume;
  };


  /*
  Returns the value of the element passed-in as a float number
   */

  SampleTypeContainerController.prototype.get_float_value = function(el, default_value) {
    var val;
    if (default_value == null) {
      default_value = 0;
    }
    val = parseFloat(el.value);
    if (isNaN(val)) {
      val = parseFloat(default_value);
    }
    return val;
  };


  /*
  Rounds a number to the given decimals number
   */

  SampleTypeContainerController.prototype.round = function(value, decimals) {
    if (decimals == null) {
      decimals = 2;
    }
    return Number(Math.round(value + 'e' + decimals) + 'e-' + decimals);
  };


  /*
  Sets the visibility of the field with the given name
   */

  SampleTypeContainerController.prototype.set_visible = function(field_name, sample_index, visible) {
    var cols_num, el, selector;
    this.debug("set_visible:field_name=" + field_name + ",sample_index=" + sample_index + ",visible=" + visible);
    selector = "div[data-fieldname='" + field_name + "']";
    if (sample_index) {
      selector = "div[data-fieldname='" + field_name + "-" + sample_index + "']";
    }
    if (sample_index === "0") {
      cols_num = document.querySelector("#ar_count");
      if (cols_num.value === "1") {
        selector = "tr[fieldname=" + field_name + "]";
      }
    }
    el = document.querySelector(selector);
    if (visible) {
      return $(el).show();
    } else {
      return $(el).hide();
    }
  };


  /*
  Fetches the object with the UID passed-in
   */

  SampleTypeContainerController.prototype.fetch = function(uid, field_names) {
    var deferred, options;
    this.debug("fetch:uid=" + uid + ",field_names=" + field_names);
    deferred = $.Deferred();
    options = {
      url: this.get_portal_url() + "/@@API/read",
      data: {
        catalog_name: "senaite_catalog_setup",
        UID: uid,
        include_fields: field_names,
        page_size: 1
      }
    };
    this.ajax_submit(options).done(function(data) {
      var object;
      object = {};
      if (data.objects) {
        object = data.objects[0];
      }
      return deferred.resolveWith(this, [object]);
    });
    return deferred.promise();
  };


  /*
  Ajax Submit with automatic event triggering and some sane defaults
   */

  SampleTypeContainerController.prototype.ajax_submit = function(options) {
    var done;
    if (options == null) {
      options = {};
    }
    this.debug("ajax_submit");
    if (options.type == null) {
      options.type = "POST";
    }
    if (options.url == null) {
      options.url = this.get_portal_url();
    }
    if (options.context == null) {
      options.context = this;
    }
    if (options.dataType == null) {
      options.dataType = "json";
    }
    if (options.data == null) {
      options.data = {};
    }
    if (options._authenticator == null) {
      options._authenticator = $("input[name='_authenticator']").val();
    }
    this.debug(">>> ajax_submit::options=", options);
    $(this).trigger("ajax:submit:start");
    done = function() {
      return $(this).trigger("ajax:submit:end");
    };
    return $.ajax(options).done(done);
  };


  /*
  Returns the portal url (calculated in code)
   */

  SampleTypeContainerController.prototype.get_portal_url = function() {
    var url;
    url = $("input[name=portal_url]").val();
    return url || window.portal_url;
  };


  /*
  Prints a debug message in console with this component name prefixed
   */

  SampleTypeContainerController.prototype.debug = function(message) {
    return console.debug("[palau.lims]", "SampleTypeController::" + message);
  };

  return SampleTypeContainerController;

})();

export default SampleTypeContainerController;

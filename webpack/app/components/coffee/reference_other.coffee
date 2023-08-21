### Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c referenceother.coffee
###

###
This controller is in charge of handling the behavior of UIDReferenceOtherFields
###
class ReferenceOtherController

  constructor: ->
    # Do no load this controller unless required
    return unless @is_required()

    @reference_other_selector = "input.reference-otherfield-check"

    # Bind the event handler to the elements
    @bind_event_handler()

    # hide/show all "Other" fields from ReferenceOtherFields
    $(el).trigger "change" for el in document.querySelectorAll @reference_other_selector

    return @

  ###
  Returns whether this controller needs to be loaded or not
  ###
  is_required: =>
     targets = ["template-ar_add", "portaltype-analysisrequest"]
     for clazz, i in document.body.classList
       if targets.includes clazz
         return true
     return false

  ###
  Binds callbacks on elements
  Attaches all the events to the body and refine the selector to delegate the
  event: https://learn.jquery.com/events/event-delegation/
  ###
  bind_event_handler: =>
    $("body").on "change", @reference_other_selector, @on_reference_other_selector_change


  ###
  Event triggered when the checkbox 'Other' is selected
  ###
  on_reference_other_selector_change: (event) =>
    el = event.currentTarget
    target_id = $(el).attr("data_target")
    target = document.querySelector("#"+target_id)
    if el.checked
      $(target).show()
    else
      $(target).hide()
      $(target).val("")


export default ReferenceOtherController
### Please use this command to compile this file into the proper folder:
coffee --no-header -w -o ../ -c reference_other.coffee
###

###
This controller is in charge of handling the behavior of ReferenceOtherWidget
###
class ReferenceOtherController

  constructor: ->
    @reference_other_selector = "input.reference-otherfield-check"
    @reference_value_selector = "div.palau-referenceother-widget-input"

    # Bind the event handler to the elements
    @bind_event_handler()

    # hide/show all "Other" fields from ReferenceOtherWidget
    for field_name in @get_field_names()
      if @has_references field_name
        el = @get_other_reference_element field_name
        el.hide()
      else
        el = @get_other_check_element field_name
        $(el).trigger "change"

    return @

  ###
  Binds callbacks on elements
  Attaches all the events to the body and refine the selector to delegate the
  event: https://learn.jquery.com/events/event-delegation/
  ###
  bind_event_handler: =>
    $("body").on "change", @reference_other_selector, @on_reference_other_selector_change
    $("body").on "select", @reference_value_selector, @on_reference_selected
    $("body").on "deselect", @reference_value_selector, @on_reference_deselected


  ###
  Returns a list of fieldnames with a reference widget bound
  ###
  get_field_names: =>
    field_names = []
    elements = document.querySelectorAll @reference_value_selector
    for element in elements
      field_names.push $(element).attr "id"
    return field_names

  ###
  Returns the HTML element where other is rendered
  ###
  get_other_reference_element: (field_name) =>
    selector = "#" + field_name + "_other_field"
    el = document.querySelector selector
    return $(el)

  ###
  Returns the HTML element where the search input is rendered
  ###
  get_search_reference_element: (field_name) =>
    selector = "div.uidreferencefield[id='"+field_name+"']"
    el = document.querySelector selector
    return $(el)

  ###
  Returns the HTML element with the other text
  ###
  get_other_check_element: (field_name) =>
    selector = "#" + field_name + "_checkbox"
    el = document.querySelector selector
    return $(el)

  ###
  Returns the HTML element with the other text
  ###
  get_other_text_element: (field_name) =>
    selector = "#" + field_name + "_other"
    el = document.querySelector selector
    return $(el)

  has_references: (field_name) =>
    selector = "textarea[name='#{ field_name }'].queryselectwidget-value"
    el = document.querySelector selector
    return unless el
    if $(el).val()
      return true
    return false

  ###
  Event triggered when the checkbox 'Other' is selected
  ###
  on_reference_other_selector_change: (event) =>
    el = event.currentTarget
    field_name = $(el).attr "data_field"
    other = @get_other_text_element field_name
    search = @get_search_reference_element field_name
    if el.checked
      # display the text box for manual entry
      other.show()
      # hide the reference widget selector
      search.hide()
    else
      # hide the text box for manual entry
      other.hide()
      other.val ""
      # display the reference widget selector
      search.show()

  ###
  Event triggered when a reference is selected
  ###
  on_reference_selected: (event) =>
    el = event.currentTarget
    field_name = $(el).attr "id"

    # Uncheck and hide the "Other" checkbox
    other_checkbox = @get_other_check_element field_name
    other_checkbox.checked = false

    other = @get_other_reference_element field_name
    other.hide()

  ###
  Event triggered when areference is deselected
  ###
  on_reference_deselected: (event) =>
    el = event.currentTarget
    field_name = $(el).attr "id"

    # Show the "Other" checkbox
    other = @get_other_reference_element field_name
    other.show()


export default ReferenceOtherController
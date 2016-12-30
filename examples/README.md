# Example experiments

This directory contains a number of example experiments that demonstrate how mouse-tracking
can be implemented in OpenSesame in different ways using the plugin:
* [mousetrap_response.osexp](mousetrap_response.osexp)
  demonstrates how the mousetrap_response item can be used
  (this experiment corresponds to the example presented in the manuscript tutorial)
* [mousetrap_response_without_forms.osexp](mousetrap_response_without_forms.osexp)
  does the same but also creates the start button screen using a `sketchpad` - `mousetrap_response` combination
  (i.e., it does not rely on `forms` in any part of the experiment)
* [mousetrap_response_shuffle_horiz.osexp](mousetrap_response_shuffle_horiz.osexp)
  demonstrates how the [advanced loop operation](http://osdoc.cogsci.nl/manual/structure/loop/#advanced-loop-operations) `shuffle_horiz` can be used to randomize the position of the response categories (left/right) in each trial
is randomized using 
* [mousetrap_response_python.osexp](mousetrap_response_python.osexp)
  demonstrates how the `MT_response` class from the mousetrap_response plug-in
  can be used in Python inline_scripts
* [mousetrap_form.osexp](mousetrap_form.osexp)
  demonstrates how the mousetrap_form plug-in can be used
* [mousetrap_form_python.osexp](mousetrap_form_python.osexp)
  demonstrates how the `MT_form` class from the mousetrap_form item
  can be used in Python inline_scripts

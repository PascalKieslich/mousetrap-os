# Example experiments

This directory contains a number of example experiments that demonstrate how mouse-tracking
can be implemented in OpenSesame in different ways using the plugin.
If would like to download all example experiments at once, you can use the following
[link](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/pascalkieslich/mousetrap-os/tree/master/examples).

* [mousetrap_response.osexp](mousetrap_response.osexp)
  demonstrates how the mousetrap_response item can be used
  (this experiment corresponds to the example presented in the manuscript tutorial)
* [mousetrap_response_without_forms.osexp](mousetrap_response_without_forms.osexp)
  does the same but also creates the start button screen using a `sketchpad` - `mousetrap_response` combination
  (i.e., it does not rely on `forms` in any part of the experiment)
* [mousetrap_response_shuffle_horiz.osexp](mousetrap_response_shuffle_horiz.osexp)
  demonstrates how the [advanced loop operation](http://osdoc.cogsci.nl/manual/structure/loop/#advanced-loop-operations)
  `shuffle_horiz` can be used to randomize the position of the response categories (left/right) in each trial
* [mousetrap_response_boundary.osexp](mousetrap_response_boundary.osexp)
  demonstrates how a dynamic start condition can be implemented 
  where the participant has to initiate a movement in order to trigger stimulus display.
  The dynamic start condition is implemented by including an additional `mousetrap_response` item
  specifying an upper boundary for tracking.
* [mousetrap_response_python.osexp](mousetrap_response_python.osexp)
  demonstrates how the `MT_response` class from the mousetrap_response plug-in
  can be used in Python inline_scripts
* [mousetrap_form.osexp](mousetrap_form.osexp)
  demonstrates how the mousetrap_form plug-in can be used
* [mousetrap_form_python.osexp](mousetrap_form_python.osexp)
  demonstrates how the `MT_form` class from the mousetrap_form item
  can be used in Python inline_scripts

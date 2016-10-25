# Mousetrap response item

The `mousetrap_response` item tracks mouse movements (and collects mouse clicks) while a stimulus is presented. Compared to the `mousetrap_form` item, it offers the most flexibility because the visual display can be designed freely. However, it requires a few steps to get started.

Importantly, the `mousetrap_response` item only handles mouse data collection and does not display any content on the screen. Rather, it relies on a different item (typically a `sketchpad`) to provide the visual display the participant sees while moving the mouse.

If you would like to use this item, you typically follow the following steps:

1. Adjusting the general settings of the experiment
2. Creating the stimulus display (e.g., using a `sketchpad`)
3. Defining the buttons (in `mousetrap_response` item)
4. Configuring the mouse-tracking options


## 1. Adjusting the general settings of the experiment

Before you start building the experiment, you should briefly check (and, if necessary, adjust) the general settings of the experiment.
They can be found in the `General properties` tab of the experiment (click on the topmost item in the `Overview` area to get there).

OpenSesame includes several `back-ends` that you can use for running the experiment.
The mousetrap items can be used together with the back-ends `legacy` and `xpyriment`.
Additional information regarding the back-ends can be found in the [OpenSesame documentation](http://osdoc.cogsci.nl/manual/backends/).

The `resolution` of the experiment should be adjusted so that it corresponds to the display resolution of the computers on which the experiment will be conducted (as it is usually desired to run the experiment in fullscreen mode).
If this resolution differs from the resolution of the computer you are using for building your experiment, you can use OpenSesame's `Run in window` mode (or `Quick run`) to test your experiment.

In addition, the option `Uniform coordinates` has to be selected.
This ensures that when recording the position of the mouse the center of the screen always corresponds to the coordinates (0,0).
This option is selected by default (unless you open an experiment that was created with an older version of OpenSesame, i.e., a version before 3.0.0).


## 2. Creating the stimulus display

When building a mouse-tracking experiment using the `mousetrap_response` item, the first step is to create the visual display that presents the stimuli to the participant.

A convenient way to do this is to use a `sketchpad` item which provides simple built-in drawing tools to create stimulus displays.
To use the `mousetrap_response` item for response collection, set the duration of the `sketchpad` to '0', and insert the `mousetrap_response` item directly after the `sketchpad`.

Creating button-like elements on a `sketchpad` item takes two steps:

1. Draw the borders of the buttons using `rect elements`. When designing the buttons, we recommend taking care that the layout is symmetrical.
2. Insert the button labels using `textline elements`. You may either use a constant string or an experimental [variable](http://osdoc.cogsci.nl/manual/variables/) (e.g., '[CategoryLeft]').


## 3. Defining the buttons

After constructing the display, the first step toward mouse-tracking is to define the number and locations of the buttons on the screen. For this, leave the `sketchpad` item and move to the adjacent `mousetrap_response` item, or insert one if you have not already done so.

The first option you need to set is the number of buttons. The `mousetrap_response` item supports up to four buttons. If you need more than four buttons, you can either use the `mousetrap_form` item or use an `inline_script` and our Python classes (see below).

Below the number of buttons, you will see a text field corresponding to each button. These fields contain the button coordinates and the button name.

The button coordinates are specified using the corresponding arguments of the `rect element` you have drawn in the previous step. To access them, you need the line of the OpenSesame script corresponding to the `rect element` that represents a button.
You can retrieve this line directly by double-clicking on the `rect element` in the `sketchpad` or by viewing the OpenSesame script of the entire `sketchpad`. In either case, the entry for a `rect element` will look similar to this:

    draw rect color=black fill=0 h=128 penwidth=1 show_if=always w=192 x=-512 y=-384 z_index=0

Of this line, only the `x` (X coordinate), `y` (Y coordinate), `w` (width), and `h` (height) arguments are of interest, i.e., `x=-512 y=-384 w=192 h=128` (the order of the arguments does not matter). Insert these into the text field. (Note: It is also possible to copy the entire line as the `mousetrap_response` item will filter it and only pick the relevant arguments.)

Apart from the coordinates, the name of the button has to be specified (as `name=text`). This value will then be saved as `response` (and `response_[item_name]`) when a participant clicks in the area of the corresponding button.
This can be done either before or after entering the coordinates. For the button name, we recommend to use whichever text content you have inserted into the button earlier (e.g., '[CategoryLeft]' in the above example).
To summarize, one of the text fields defining a button might contain the following arguments:

	x=-512 y=-384 w=192 h=128 name=[CategoryLeft]

Repeat this step for each button you wish to include, varying coordinates and name accordingly.


## 4. Configuring the mouse-tracking options

### Correct button name

`Correct button name` can be used to specify the name of the button corresponding to the correct response (as a string or an experimental `[variable]`). If specified, participants' responses are classified as correct (or not) depending on whether the name of the button participants clicked corresponds to the value in this field. OpenSesame will also populate the variable `correct` (and `correct_[item_name]`) with either '1' (given response matches correct response) or '0' (no match).


### Update feedback variables

OpenSesame automatically keeps track of a number of [feedback variables](http://osdoc.cogsci.nl/manual/variables/#feedback-variables), such as the overall `accuracy` and the `average_response_time`.
If these global feedback variables should be updated based on the response to the `mousetrap_response` item, please check the corresponding box.


### Reset mouse position on trial start

To increase the comparability between trials, you can reset the mouse position to a given coordinate when the tracking begins.

To do this, check the box `Reset mouse position when tracking starts`. Next, enter the desired x and y coordinates as `Start coordinates`.
Coordinates are given in the metric of the `sketchpad` ('0;0' corresponding to the screen center), and are separated by semicolon, comma, or space.

When a new `mousetrap_response` item is created, the values are preset so they correspond to the center of the button on a `form_text_display` item (this way, such an item can be used as a start item in the beginning of each trial without further adjustment).


### Timeout

The response timeout (number of milliseconds, or 'infinite' for no timeout) is indicated under `Timeout`. After this interval, OpenSesame will stop tracking and move on to the next item.


### Stopping boundaries

`Stopping boundaries` can be used for specifying vertical or horizontal boundaries on the screen. If the mouse crosses one of the boundaries, OpenSesame will stop tracking and move on to the next item. This can be helpful, e.g., if a stimulus should only be displayed once the mouse passes a certain threshold. Boundaries are specified in sketchpad metric (or 'no', if no checking should be performed for a specific boundary).


### Response options

By default, participants are expected to click within the area of a button (as shown onscreen) to respond.
The (physical) mouse buttons that can be used to indicate a response are specified in the field `Allowed mouse buttons`.
Each mouse button can be specified using its number or name, as in the standard [mouse_response](http://osdoc.cogsci.nl/manual/response/mouse/#mouse-button-names) item.
If several mouse buttons are permitted, their corresponding values can be enumerated, separated by a semicolon, comma, or space.

Participants could also simply be allowed to indicate the choice of an option by entering the corresponding area of the button with the cursor (no click is required).
To allow this, uncheck the option `Click required to indicate response`.


### Warning message if maximum initiation time is exceeded

You may want to display a warning message when a participant hesitates to initiate a mouse movement.
To allow this, the `mousetrap_response` item automatically computes the initiation time (i.e., the time [in ms] until a mouse movement is initiated) and saves it in the variable `initiation_time` (and `initiation_time_[item_name]`).
This variable can be used, for example, in a `Run if` condition (e.g., `[initiation_time]>2000`), to display a `sketchpad` containing a warning message **after** the decision was made.

If a warning message should be displayed **immediately** on the `sketchpad` once the time limit is exceeded, check the box `Display warning message immediately if maximum initiation time is exceeded`.

Next, indicate the `Maximum initiation time` (in milliseconds).
If the mouse has not been moved within this time period, the warning message will be shown.
Please note that OpenSesame will only check for mouse movements in increments of the logging resolution time.

The `Warning message` can be specified using the OpenSesame script syntax for textline elements. Besides, the name of the current `sketchpad` needs to be specified explicitly as an additional argument.

A complete example could look like this:

	draw textline center=1 color=red text="Please start moving" x=0 y=0 sketchpad=present_stimulus

This means that the text 'Please start moving' will be displayed in red at the center of the current `sketchpad` (which is named 'present_stimulus'), once the initiation time limit passes without mouse movement.


### Logging resolution

The `Logging resolution` specifies the interval (in milliseconds) in which the mouse position is recorded. By default, this takes place every 10 ms (corresponding to a 100 Hz sampling rate).
The actual resolution may differ depending on the performance of the hardware. The achieved rate can be seen in the data, as a timestamp is saved for each recorded position.



## Mouse-tracking data

### Data logging in OpenSesame

The mouse-tracking data will be stored in three variables. Each variable contains a list of values (separated by ', ') - one entry for each recorded position of the mouse. The position coordinates are given in pixels, whereby (0,0) corresponds to the center of the screen and values increase as the mouse moves toward the bottom right:

* `timestamps_[item_name]` contains the timestamps
* `xpos_[item_name]` contains the x-coordinates
* `ypos_[item_name]` contains the y-coordinates

Note that (as in other OpenSesame items) the stored data will only be written into a log file if a logger item is included after the item.


### Processing and analyzing the data

The authors have developed several `R packages` (available on CRAN) that can be used for further processing the recorded data.

The [readbulk R package](https://github.com/pascalkieslich/readbulk) provides the `read_opensesame` function for merging data from several participants (and for reading them into R as one large data frame).

The [mousetrap R package](https://github.com/pascalkieslich/mousetrap) provides a number of functions for preprocessing, analyzing, and visualizing mouse-tracking data. It contains, among other things, a specific function (`mt_import_mousetrap`) for importing mouse-tracking data recorded using the mousetrap items in OpenSesame.


## Alternative uses for mousetrap response

### Making sketchpads interactive

The standard way to implement interactive displays with buttons in OpenSesame is by using the [form plugins](http://osdoc.cogsci.nl/manual/forms/about/).

The current item allows you to include button-like interactions using the `sketchpad` item (following the procedure outlined above).
In case that this is your primary interest and you are not interested in saving the mouse-tracking data (the mouse-tracking data will considerably increase the size of the logfile), you can uncheck the box `Save mouse-tracking data`.

One typical application might be the display of a start screen with a start button before the actual stimuli are presented and the mouse-tracking procedure starts.


### Importing the MT_response class for Python inline_scripts

The `mousetrap_response` item loads the `PyMT_response` package which includes the `MT_response` class.
The `MT_response` class can be used in Python `inline_scripts` to implement mouse-tracking
(typically in combination with a [canvas](http://osdoc.cogsci.nl/manual/python/canvas/) object).

To make the `MT_response` class available, the `mousetrap_response` item has to be inserted at the beginning of the experiment.
As it is only needed for this purpose, the option `Skip item and only load package` needs to be checked.
After this, the `MT_response` class can be imported in an `inline_script` by entering:

	from PyMT_response import MT_response
    
To get an impression how the MT_response class can be used, please see the 'mousetrap_response_python.osexp' example experiment provided online in the [examples folder](https://github.com/pascalkieslich/mousetrap-os/tree/master/examples) of the [mousetrap-os GitHub repository](https://github.com/pascalkieslich/mousetrap-os). Once the `MT_response` class has been imported, the documentation of the central functions can be accessed using:

    ?MT_response
    ?MT_response._exec

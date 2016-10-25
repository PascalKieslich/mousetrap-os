# Mousetrap form item

The `mousetrap_form` item allows tracking of mouse movements (and collection of mouse clicks) in custom `forms`. Compared to the `mousetrap_response` item, it offers the possibility to directly define the stimulus presentation within the item by using a form (including interactive elements, such as `buttons` and `image_buttons`). However, it does not provide a graphical interface for stimulus creation, and instead uses the OpenSesame script syntax. Technically, the `mousetrap_form` item is a modification and extension of the [form_base plugin](http://osdoc.cogsci.nl/manual/forms/custom/#creating-forms-using-opensesame-script).

The general layout of the form as well as the mouse-tracking specific options can be adjusted in the control tab. This is also the tab that is displayed first when clicking on the item.
The specific widgets on the form (e.g., buttons and text) can be added using OpenSesame script (click on `Select view` in the top-right corner of the item and select `View script`).

If you would like to use this item, you will typically follow the following steps:

1. Adjusting the general settings of the experiment
2. Specifying the general layout of the form (`Controls`)
3. Creating the widgets (`OpenSesame script`)
4. Configuring the mouse-tracking options (`Controls`)


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


## 2. Setting the general layout of the form (Controls)

To specify the layout of the form, use the control options `Number of columns` and `Number of rows`.
This will set up a grid with the specified number of columns and rows, on which the form content can be placed.

In our experience, users often find it helpful if the grid is made up of square cells. To achieve this, the ratio of the number of columns and number of rows should match the aspect ratio of the experiment’s resolution (width/height).
To make this even easier, the item initially selects the number of columns and rows based on the display resolution specified in the experiment, so that square cells result by default.

Unlike the general `form_base`, the `mousetrap_form` removes all margins and spacing between cells (i.e., the first grid cell starts directly in the top left corner of the screen, and grid cells are not separated by a margin).

As other `forms`, `mousetrap_form` supports theming (i.e., different themes for the general layout of the form).
You can choose between different `Themes` using the corresponding option.


## 3. Creating the widgets (OpenSesame script)

The specific elements on the form (e.g., buttons and text) are called `widgets`. They are specified using OpenSesame script.
To access the item's OpenSesame script, click on `Select view` in the top-right corner of the item and select `View script`.
As you will see, the control options themselves already have generated several script lines which represent the options available through the interface (and can be ignored).

Every widget on the form is defined in its own line starting with `widget`.
The general syntax is as follows:

    widget [column] [row] [column span] [row span] [widget type] [options]

The columns and rows of the grid are numbered starting with 0,0 in the top left corner. `Column` and `row` indicate the column and row where the upper left corner of the widget will be placed.

`Column span` and `row span` indicate the size of the widget in grid columns and rows. These can be set to 1 or any higher value.

`Widget type` indicates the type of widget that should be created. An overview of the different widget types is given in the [OpenSesame documentation](http://osdoc.cogsci.nl/manual/forms/custom/#available-widgets-and-keywords). The widgets you will use most are likely `labels` and `buttons`.

Following the widget type, widget-type specific options can be specified, each starting with the name of the argument, followed by an equal sign and the value of the argument. Multiple arguments are separated by spaces.

A very simple, but complete, mouse-tracking form (assuming a grid with 12 columns and 9 rows) could look like this:

    widget 4 7 4 1 label text="Please choose A or B"
    widget 0 0 2 1 button text="Option A"
    widget 10 0 2 1 button text="Option B"

In this script, three widgets are created:
One label is created in the bottom center of the screen; it displays the task instruction. The text keyword contains the text that should be displayed. In addition, two buttons are created in the top left and top right corners of the screen displaying the corresponding response options (`Option A` and `Option B`).

To format the text, OpenSesame supports a subset of [HTML tags](http://osdoc.cogsci.nl/manual/stimuli/text/).
The following option, for example, creates a text in red color with font size 28:

    text="<span color='red' size ='28'>Please choose A or B</span>"

Besides static text, you can use experimental variables at any point during the script, by simply entering the name of the experimental variable in square brackets. Assuming that the labels of the response options are already specified (e.g., in a loop), you could write:

    widget 4 7 4 1 label text="[Exemplar]"
    widget 0 0 2 1 button text="[CategoryLeft]"
    widget 10 0 2 1 button text="[CategoryRight]"


When designing the layout of the form for a mouse-tracking experiment, we recommend taking care that the layout is symmetrical, particularly with respect to the position of the buttons.


## 4. Configuring the mouse-tracking options (Controls)


### Correct button name

`Correct button name` can be used to specify the name of the button corresponding to the correct response (as a string or an experimental `[variable]`). If specified, participants' responses are classified as correct (or not) depending on whether the name of the button participants clicked corresponds to the value in this field. OpenSesame will also populate the variable `correct` (and `correct_[item_name]`) with either '1' (given response matches correct response) or '0' (no match).


### Update feedback variables

OpenSesame automatically keeps track of a number of [feedback variables](http://osdoc.cogsci.nl/manual/variables/#feedback-variables), such as the overall `accuracy` and the `average_response_time`.
If these global feedback variables should be updated based on the response to the `mousetrap_form` item, please check the corresponding box.


### Reset mouse position on trial start

To increase the comparability between trials, you can reset the mouse position to a given coordinate when the tracking begins.

To do this, check the box `Reset mouse position when form is shown`. Next, enter the desired x and y coordinates as `Start coordinates`.

The `Start coordinates` can be entered as two numbers (separated by semicolon, comma, or space), corresponding to the position of the mouse on the grid (column, row).

If the start coordinates are integers, the mouse will be reset on the left upper corner of the grid cell at the specified coordinates.
Positions within this cell can be achieved by adding decimals, which will be used to move fractions of the cell's width and height. For example, if the mouse should be placed halfway between column 6 and 7, enter 6.5.

When a new `mousetrap_form` item is created, the values are preset so they correspond to the center of the button on a `form_text_display` item (this way, such an item can be used as a start item  in the beginning of each trial without further adjustment).


### Timeout

The response timeout (number of milliseconds, or 'infinite' for no timeout) is indicated under `Timeout`. After this interval, OpenSesame will stop tracking and move on to the next item.


### Response options

Participants can indicate their responses in several ways.

By default, participants are expected to click within the area of a button (as shown onscreen) to respond.
The (physical) mouse buttons that can be used to indicate a response are specified in the field `Allowed mouse buttons`.
Each mouse button can be specified using its number or name, as in the standard [mouse_response](http://osdoc.cogsci.nl/manual/response/mouse/#mouse-button-names) item.
If several mouse buttons are permitted, their corresponding values can be enumerated, separated by a semicolon, comma, or space.

Participants could also simply be allowed to indicate the choice of an option by entering the corresponding area of the button with the cursor (no click is required).
To allow this, uncheck the option `Click required to indicate response`.


### Warning message if maximum initiation time is exceeded

You may want to display a warning message when a participant hesitates to initiate a mouse movement.
To allow this, the `mousetrap_form` item automatically computes the initiation time (i.e., the time [in ms] until a mouse movement is initiated) and saves it in the variable `initiation_time` (and `initiation_time_[item_name]`).
This variable can be used, for example, in a `Run if` condition (e.g., `[initiation_time]>2000`), to display a sketchpad containing a warning message **after** the decision was made.

If a warning message should be displayed **immediately** on the form once the time limit is exceeded, check the box `Display warning message immediately if maximum initiation time is exceeded`.

Next, indicate the `Maximum initiation time` (in milliseconds).
If the mouse has not been moved within this time period, the warning message will be shown.
Please note that OpenSesame will only check for mouse movements in increments of the logging resolution time.

To specify the `Warning message`, you need to specify a widget in OpenSesame script syntax.
A simple example for a warning message could look like this:

    widget 4 5 4 1 label text="<span color='red'>Please start moving</span>"


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


## Alternative uses for mousetrap form

### Implement modified version of form base

The `mousetrap_form` can also be used in place of the standard `form_base`, even if mouse tracking is not desired. This offers several advantages:

* The form layout is simplified (see above).
* The form automatically logs `response` and `response_time` variables.
* The form optionally determines the correctness of the response and updates the global feedback variables.

In case the form is only used for one of these reasons and you are not interested in saving the mouse-tracking data (the mouse-tracking data will considerably increase the size of the logfile), you can uncheck the box `Save mouse-tracking data`.

The form can be used together with the following widgets:

* `Button`
* `Label`
* `Image`
* `Image_button`

Note that additional interactive widgets (e.g., `checkboxes`) might not be compatible with the `mousetrap_form` item.


### Importing the MT_form class for Python inline_scripts

The `mousetrap_form` item loads the `PyMT_form` package which includes the `MT_form` class.
Similar to the general [form](http://osdoc.cogsci.nl/manual/forms/widgets/form/) class,
the `MT_form` class can be used in `inline_scripts` to create a mouse-tracking-form in Python.

To make the `MT_form` class available, the `mousetrap_form` item has to be inserted at the beginning of the experiment.
As it is only needed for this purpose, the option `Skip item and only load package` needs to be checked.
After this, the `MT_form` class can be imported in an `inline_script` by entering:

    from PyMT_form import MT_form

To get an impression how the MT_form class can be used, please see the 'mousetrap_form_python.osexp' example experiment provided online in the [examples folder](https://github.com/pascalkieslich/mousetrap-os/tree/master/examples) of the [mousetrap-os GitHub repository](https://github.com/pascalkieslich/mousetrap-os). Once the `MT_form` class has been imported, the documentation of the central functions can be accessed using:
    
    ?MT_form
    ?MT_form._exec

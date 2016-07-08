# Mousetrap plug-ins for OpenSesame

__Easily build mouse-tracking experiments with OpenSesame.__


The Mousetrap package provides two plug-ins that implement mouse-tracking in [OpenSesame](http://osdoc.cogsci.nl/).
Both plug-ins offer different ways of implementing mouse-tracking:

![alt text](plugins/mousetrap_response/mousetrap_response_large.png "mousetrap_response plug-in") The [mousetrap_response plug-in](plugins/mousetrap_response/mousetrap_response.md) tracks mouse movements while another stimulus (e.g., a sketchpad) is presented.

![alt text](plugins/mousetrap_form/mousetrap_form_large.png "mousetrap_form plug-in") The [mousetrap_form plug-in](plugins/mousetrap_form/mousetrap_form.md) allows tracking of mouse movements in custom forms specified using OpenSesame script.

More information about each plug-in can be found in the corresponding helpfiles (as linked above).
Besides, a number of example experiments that demonstrate the basic features of the plug-ins can be found in the [examples folder](examples).

Once data have been collected with the plug-ins, the data can be processed, analyzed and visualized using the [mousetrap R package](https://github.com/PascalKieslich/mousetrap).


## General information
The Mousetrap plug-ins are developed by Pascal Kieslich and Felix Henninger.
They are published under the [GNU General Public License (version 3)](LICENSE).

## Installation
To install the plug-ins, please [download the latest release](https://github.com/PascalKieslich/mousetrap-os/releases).
Once downloaded (and unzipped), the plug-ins can be installed by copying the content of the plugins folder into one of the folders that OpenSesame searches for plug-ins
(e.g., under Windows the "share\opensesame_plugins" folder in the OpenSesame installation directory).
More information about installing plug-ins can be found on the [OpenSesame homepage](http://osdoc.cogsci.nl/manual/environment/#installing-plugins-and-extensions).

## Acknowledgments
Mousetrap extends the many useful features of OpenSesame developed by the [OpenSesame development team](http://osdoc.cogsci.nl/team/) led by [Sebastiaan Mathôt](http://www.cogsci.nl/smathot).
Mousetrap uses (modified) icons from the [Faenza Icon Set (by Titheum)](http://tiheum.deviantart.com/art/Faenza-Icons-173323228). We thank Anja Humbs for testing a development version of the plug-ins.

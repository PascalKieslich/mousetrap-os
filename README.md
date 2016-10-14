# Mousetrap plug-ins for OpenSesame

__Easily build mouse-tracking experiments with OpenSesame.__

[![DOI](https://zenodo.org/badge/22029/PascalKieslich/mousetrap-os.svg)](https://zenodo.org/badge/latestdoi/22029/PascalKieslich/mousetrap-os)

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

### Latest stable version

Please run the following commands in OpenSesame's [debug window](http://osdoc.cogsci.nl/3.1/manual/interface/#the-debug-window):

    import pip
    pip.main(['install', 'https://github.com/PascalKieslich/mousetrap-os/archive/stable.zip'])

The [installation of plug-ins](http://osdoc.cogsci.nl/manual/environment/#installing-plugins-and-extensions) is covered in more detail in the OpenSesame documentation, which also covers alternate methods.

[Release notes](https://github.com/PascalKieslich/mousetrap-os/releases/latest) for this version are available, as for all [previous releases](https://github.com/PascalKieslich/mousetrap-os/releases).

### Development version

To install the latest development version, please run the following commands in the OpenSesame debug window:

    import pip
    pip.main(['install', 'https://github.com/PascalKieslich/mousetrap-os/archive/master.zip'])

## Acknowledgments
Mousetrap extends the many useful features of OpenSesame developed by the [OpenSesame development team](http://osdoc.cogsci.nl/team/) led by [Sebastiaan Mathôt](http://www.cogsci.nl/smathot).
Mousetrap uses modified icons from the [Moka Icon Theme (by Sam Hewitt)](https://snwh.org/moka). We thank Anja Humbs for testing a development version of the plug-ins.

# Mousetrap plugin for OpenSesame

__Easily build mouse-tracking experiments with OpenSesame.__

[[Installation]](#installation) [[Examples]](examples#example-experiments) [[Forum]](http://forum.cogsci.nl/index.php?p=/categories/mousetrap) [[Paper]](https://doi.org/10.3758/s13428-017-0900-z)

The mousetrap plugin provides two items that implement mouse-tracking in [OpenSesame](http://osdoc.cogsci.nl/).
Both offer different ways of implementing mouse-tracking:

![alt text](plugins/mousetrap_response/mousetrap_response_large.png "mousetrap_response plug-in") The [mousetrap_response item](plugins/mousetrap_response/mousetrap_response.md#mousetrap-response-item) tracks mouse movements while another stimulus (e.g., a sketchpad) is presented.

![alt text](plugins/mousetrap_form/mousetrap_form_large.png "mousetrap_form plug-in") The [mousetrap_form item](plugins/mousetrap_form/mousetrap_form.md#mousetrap-form-item) allows tracking of mouse movements in custom forms specified using OpenSesame script.

More information about each item can be found in the corresponding helpfile (as linked above).

Once data have been collected with the mousetrap plugin, the data can be processed, analyzed and visualized using the [mousetrap R package](https://github.com/PascalKieslich/mousetrap).


## General information
Mousetrap is developed by Pascal Kieslich and Felix Henninger.
Questions about using mousetrap can be asked in the [forum](http://forum.cogsci.nl/index.php?p=/categories/mousetrap).

It is published under the [GNU General Public License (version 3)](LICENSE).

If you use mousetrap in your published research, we kindly ask that you cite it as follows:

> Kieslich, P. J., & Henninger, F. (2017). Mousetrap: An integrated, open-source mouse-tracking package. _Behavior Research Methods, 49_(5), 1652-1667. https://doi.org/10.3758/s13428-017-0900-z


## Installation

Please select which `mousetrap-os` version to install depending on which OpenSesame version you are using:
* For OpenSesame versions 3.3.0 to 3.3.14, install the [latest stable version](#latest-stable-version)
* For OpenSesame versions 4.0.0 or later, install the [current development version](#development-version)

### Current stable version

To install the current stable release, please run the following commands in OpenSesame's [debug window](http://osdoc.cogsci.nl/manual/interface/#the-debug-window):

```python
!pip install https://github.com/PascalKieslich/mousetrap-os/archive/refs/tags/2.1.0.zip
```

You'll need to restart OpenSesame after the installation for the mousetrap items to work.

If the installation fails due to missing write access, you may have to run OpenSesame with administrator privileges for the installation (on Windows, right-click the OpenSesame program icon and select "Run as Administrator").

[Release notes for the latest version](https://github.com/PascalKieslich/mousetrap-os/releases/latest) are available, as for all [previous releases](https://github.com/PascalKieslich/mousetrap-os/releases).

### Development version

To install the latest development version in OpenSesame 3.3.0 or later, please follow the above instructions, replacing the command with the following (which is still entered in OpenSesame's [debug window](http://osdoc.cogsci.nl/manual/interface/#the-debug-window)):

```python
!pip install https://github.com/PascalKieslich/mousetrap-os/archive/master.zip
```

## Examples

A number of example experiments that demonstrate the basic features of the items can be found in the [examples folder](examples#example-experiments).


## Validation

The results from a technical validation of the plugin can be found in the [validation folder](validation).


## Acknowledgments
Mousetrap extends the many useful features of OpenSesame developed by the [OpenSesame development team](http://osdoc.cogsci.nl/team/) led by [Sebastiaan Mathôt](http://www.cogsci.nl/smathot).
Mousetrap uses modified icons from the [Moka Icon Theme (by Sam Hewitt)](https://snwh.org/moka). We thank Anja Humbs for testing a development version. This work was supported by the University of Mannheim’s Graduate School of Economic and Social Sciences, which is funded by the German Research Foundation.

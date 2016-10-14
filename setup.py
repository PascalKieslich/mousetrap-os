from setuptools import setup, find_packages

long_description = """
Mousetrap plug-ins for OpenSesame
=================================

**Easily build mouse-tracking experiments with OpenSesame.**

The Mousetrap package provides two plug-ins that implement mouse-tracking in `OpenSesame <http://osdoc.cogsci.nl/>`_. Both plug-ins offer different ways of implementing mouse-tracking:

The `mousetrap_response plug-in`_ tracks mouse movements while another stimulus (e.g., a sketchpad) is presented.

The `mousetrap_form plug-in`_ allows tracking of mouse movements in custom forms specified using OpenSesame script.

More information about each plug-in can be found in the corresponding helpfiles (as linked above). Besides, a number of example experiments that demonstrate the basic features of the plug-ins can be found in the `examples folder`_.

Once data have been collected with the plug-ins, the data can be processed, analyzed and visualized using the `mousetrap R package`_.

.. _OpenSesame: http://osdoc.cogsci.nl/
.. _mousetrap_response plug-in: https://github.com/PascalKieslich/mousetrap-os/blob/master/plugins/mousetrap_response/mousetrap_response.md
.. _mousetrap_form plug-in: https://github.com/PascalKieslich/mousetrap-os/blob/master/plugins/mousetrap_form/mousetrap_form.md
.. _examples folder: https://github.com/PascalKieslich/mousetrap-os/blob/master/examples
.. _mousetrap R package: https://github.com/PascalKieslich/mousetrap
"""

def list_files(path):
    import glob, os

    return [f for f in glob.glob(path)
        if os.path.isfile(path) and not f.endswith('.pyc')]

setup(
    name="mousetrap-os",

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version = '1.1.5',

    description = "Mousetrap plug-ins for OpenSesame",
    long_description = long_description,

    # The project's main homepage.
    url = 'https://github.com/PascalKieslich/mousetrap-os',

    # Author details
    author = 'Pascal Kieslich & Felix Henninger',
    author_email = 'kieslich@psychologie.uni-mannheim.de',

    # License
    license = 'GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        # Status
        'Development Status :: 5 - Production/Stable',

        # Audience
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',

        # License
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Python version support
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],

    # Package information
    # For now, we are installing all files as supplementary data
    #package_dir = {'mousetrap-os': 'plugins'},
    #packages = find_packages(exclude='examples'),

    # OpenSesame packages are installed as auxiliary data
    data_files = [
        # Files are hard-coded for now
        #('share/opensesame_plugins/mousetrap_form', list_files('plugins/mousetrap_form/*')),
        #('share/opensesame_plugins/mousetrap_response', list_files('plugins/mousetrap_response/*')),
        #('share/opensesame_plugins/mousetrap_form/PyMT_form', list_files('plugins/mousetrap_form/PyMT_form/*')),
        #('share/opensesame_plugins/mousetrap_response/PyMT_response', list_files('plugins/mousetrap_response/PyMT_response/*')),
        ('share/opensesame_plugins/mousetrap_form', [
            'plugins/mousetrap_form/info.yaml',
            'plugins/mousetrap_form/mousetrap_form.md',
            'plugins/mousetrap_form/mousetrap_form.png',
            'plugins/mousetrap_form/mousetrap_form.py',
            'plugins/mousetrap_form/mousetrap_form_large.png',
            'plugins/mousetrap_form/PyMT_form/__init__.py'
        ]),
        ('share/opensesame_plugins/mousetrap_form/PyMT_form', [
            'plugins/mousetrap_form/PyMT_form/__init__.py'
        ]),
        ('share/opensesame_plugins/mousetrap_response', [
            'plugins/mousetrap_response/info.yaml',
            'plugins/mousetrap_response/mousetrap_response.md',
            'plugins/mousetrap_response/mousetrap_response.png',
            'plugins/mousetrap_response/mousetrap_response.py',
            'plugins/mousetrap_response/mousetrap_response_large.png',
            'plugins/mousetrap_response/PyMT_response/__init__.py'
        ]),
        ('share/opensesame_plugins/mousetrap_response/PyMT_response', [
            'plugins/mousetrap_response/PyMT_response/__init__.py'
        ]),
    ]

)

## Overview

This repository is for Python code intended to be shared across projects. Good things to put here are general utility
functions, infrastructure components free of business logic, and the like.

To add common to your project, add this to your `requirements.txt`:

    -e git+https://github.com/PolymathVentures/common@0.1.2#egg=common

Common uses Git tags -- such as the "0.1.2" above -- to mark releases. The latest tag should always match the version in 
`setup.py`. Always point to tags, not commits!

Currently this repository is public to make it especially easy to install and not take up a private slot in our 
GitHub plan. If this repository needs to be made private, you can insert an appropriate GitHub access token into
the URL above to enable password-free installation.

## Dependencies

Note that common does add some dependencies to your project. They are listed in the [setup.py file](setup.py#L12-L17).
Be mindful about adding new ones as they will have to be installed in all projects using common.

Since this is a library intended for use in other apps, the way dependencies work is a bit different. There is no
`requirements.txt`; instead you need to work more directly with setuptools and it's main configuration file `setup.py`.
Here are the absolute basics you need to know:

 * Dependencies needed by common must be listed in the `install_requires` section.
 * Packages importable from common must be listed in the `packages` section.

See the [Packaging and Distributing Projects](https://python-packaging-user-guide.readthedocs.org/en/latest/distributing/)
section of the Python Packaging User Guide to learn more.

## Development

To install into an existing virtual environment, such as when testing new common code in your app, the easiest way to do
it to [install from a local source tree](https://python-packaging-user-guide.readthedocs.org/en/latest/installing/#installing-from-a-local-src-tree):

    $ pip install -e /path/to/common/on/your/system

This creates a link to common in your virtual environment:

    $ cat venv/lib/python3.4/site-packages/common.egg-link
    /path/to/common/on/your/system

Any changes in common will be reflected immediately in your virtual environment.

To remove the link and uninstall common:

    $ pip uninstall common

If you want to actually install common into your virtual environment instead of linking to it, do this *while in your
app's virtual environment*:

    $ cd /path/to/common/on/your/system
    $ python setup.py install

If you go this route instead of the link it can sometimes be difficult to know if you have installed a version of
common with your latest changes. To be sure, either bump the version in `setup.py` or uninstall common before running
`python setup.py install`.

## Release

When you wish to publish a new version of common, bump the version number in `setup.py` and push a new tag that matches
that version:

    $ grep version setup.py
    version='0.1.5',
    $ git tag 0.1.5
    $ git push origin --tags

## Build status 

[![Circle CI](https://circleci.com/gh/PolymathVentures/common.svg?style=svg)](https://circleci.com/gh/PolymathVentures/common)

## Overview

This repository is for Python code intended to be shared across projects. Good things to put here are general utility
functions and infrastructure components free of business logic.

To include common in your app add the following to your `requirements.txt`:

    -e git+https://github.com/PolymathVentures/common@0.1.2#egg=common

Common uses Git tags -- e.g. "0.1.2" above -- to mark releases. The latest tag should always match the version in 
`setup.py`. Always point to tags, not commits!

Currently this repository is public to make it especially easy to install and not take up a private slot in our 
GitHub plan. If this repository needs to be made private, you can insert an appropriate GitHub access token into
the URL above to enable password-free installation.

## Dependencies

Note that common adds dependencies to your app. They are listed in the [setup.py file](setup.py#L12-L17).
Be mindful of adding new dependencies as they will have to be installed in all apps that use common.

Since this is a library intended for use in other apps, the way dependencies work is a bit different. There is no
`requirements.txt`; instead you need to work more directly with setuptools and it's configuration file `setup.py`.
Here are the absolute basics you need to know:

 * Dependencies of common go in the `install_requires` section of `setup.py`.
 * Packages importable from common go in the `packages` section of `setup.py`.

See the [Packaging and Distributing Projects](https://packaging.python.org/distributing/)
section of the Python Packaging User Guide to learn more.

## Development

To install into an existing virtual environment, such as when testing new common features in your app, the easiest way is to [install from a local source tree](https://packaging.python.org/installing/#installing-from-a-local-src-tree):

    $ pip install -e /path/to/common/on/your/system

This creates a link to common in your virtual environment:

    $ cat venv/lib/python3.5/site-packages/common.egg-link
    /path/to/common/on/your/system

Any changes in common will be reflected immediately in your virtual environment.

To remove the link and uninstall common:

    $ pip uninstall common

If you want to actually install common into your virtual environment instead of linking, run this *while in your virtual environment*:

    $ cd /path/to/common/on/your/system
    $ python setup.py install

If you go this route instead of linking it can sometimes be difficult to know if you have installed a version of
common with your latest changes. To be sure, either bump the version in `setup.py` or uninstall common before running
`python setup.py install`.

To run the tests:
    
    $ python setup.py test

## Release

When you wish to publish a new version of common, bump the version number in `setup.py` and push a new tag that matches
that version:

    $ grep version setup.py
    version='0.1.5',
    $ git tag 0.1.5
    $ git push origin --tags

se agrega el action para backup del codigo en S3

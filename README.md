## Overview

This repository is for Python code intended to be shared across projects. Good things to put here are general utility
functions, infrastructure components free of business logic, and the like.

To add common to your project, add this to your "requirements.txt":

    -e git+https://github.com/PolymathVentures/common@0.1.2#egg=common

Common uses Git tags -- such as the "0.1.2" above -- to mark releases. The latest tag should always match the version in 
"setup.py". Always point to tags, not commits!

Currently this repository is public to make it especially easy to install and not take up a private slot in our 
GitHub plan. If this repository needs to be made private, you can insert an appropriate GitHub access token into
the URL above to enable password-free installation.

Note that common adds dependencies. See the "setup.py" file -- currently it's just Flask and pytz. Be mindful about 
adding new ones as they will have to be installed in all projects using common.

## Development

To install into an existing virtual environment, such as when developing or testing common code:

    pip uninstall common
    python setup.py install
    
When developing locally it can sometimes be difficult to know if you have installed a version of common with your 
latest changes. To be sure, either always bump the version in "setup.py" or always uninstall common before running 
`python setup.py install`.

## Release

When you wish to publish a new version of common, bump the version number in "setup.py" and push a new tag that matches 
that version:

    git tag 0.1.3
    git push origin --tags

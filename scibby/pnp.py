#!/usr/bin/env python
import sys
import os.path

from twisted.python.modules import iterModules

from scibby.client import configuration

sys.path.append(configuration["plugins_directory"])

plugins = {}

# Get list of all plugins and import them
# TODO make the modules be packages and have a file describing them as an actual
# scibby plugin so not everything in this directory gets imported
for modinfo in iterModules():
    if os.path.dirname(modinfo.filePath.path) == configuration["plugins_directory"]:
        filename = os.path.basename(modinfo.filePath.path)
        modulename = os.path.splitext(filename)[0]

        plugins[modulename] = __import__(modulename, globals(), locals())

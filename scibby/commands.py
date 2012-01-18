#!/usr/bin/env python
from twisted.web.client import getPage

import lxml.html
import random

import operator

from scibby import pnp

try:
    import json
except ImportError:
    import simplejson as json


"""Commands container, to be replaced with a plugin way of dealing with things
later on the lifecycle of scibby the irc bot!"""

def plugins(rest):
    # TODO list all enabled plugins found by scibby.plugins
    return ", ".join(plugins.keys())

def about(rest):
    # TODO more verbose
    return "https://github.com/ikanobori/scibby"

def usage(rest):
    return "!{%s}" % ", ".join(whitelist.keys())

def akali(rest):
    return "http://i.imgur.com/3e8hp.jpg"

whitelist = {"plugins": plugins, "about": about, "usage": usage, "akali": usage}

def _handler(rest):
    print rest

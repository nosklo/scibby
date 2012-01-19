import os
import sys
from ConfigParser import ConfigParser

class Struct(object):
    """Simple class for instantiating objects we can add arbitrary attributes
    to and use for various arbitrary things."""

def get_config_home():
    """Returns the base directory for scibby's configuration files."""
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME", "~/.config")
    return os.path.join(xdg_config_home, 'scibby')

def default_config_path():
    """Returns scibby's default configuration file path."""
    return os.path.join(get_config_home(), "config")

def fill_config_with_default_values(config, default_values):
    for section in default_values.iterkeys():
        if not config.has_section(section):
            config.add_section(section)

        for (opt, val) in default_values[section].iteritems():
            if not config.has_option(section, opt):
                config.set(section, opt, str(val))

def loadini(struct, configfile):
    """Load ini and store in struct"""

    config_path = os.path.expanduser(configfile)

    config = ConfigParser()

    fill_config_with_default_values(config, {
        "general": {
            "host": "irc.quakenet.org",
            "port": 6667,
            "channels": "#scibbytest",
            "nickname": "scabby",
            "plugins_directory": "~/dev/src/scibby-plugins"
        }})

    config.read(config_path)

    struct.host = config.get("general", "host")
    struct.port = config.getint("general", "port")
    struct.channels = config.get("general", "channels").split(",")
    struct.nickname = config.get("general", "nickname")
    struct.plugins_directory = config.get("general", "plugins_directory")

    return struct

values = loadini(Struct(), default_config_path())

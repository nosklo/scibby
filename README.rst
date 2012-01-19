Scibby
######

About
=====
Scibby is a plugin based IRC bot written in Python, using Twisted.

Installation
============
Download source code, unpack.

In the scibby directory run `python -m scibby.client` or run the run_scibby.sh script to
start it daemonized.

Configuration
=============
Make a ~/.config/scibby/config file, the section is called [general], you can configure:
- host
- port
- channels (comma seperated list)
- nickname
- plugins_directory (defaults to ~/.scibby/plugins)

#!/usr/bin/env python
from twisted.web.client import getPage

import lxml.html

"""Commands container, to be replaced with a plugin way of dealing with things
later on the lifecycle of scibby the irc bot!"""

### URL commands ###
def command_title(url):
    """Use lxml to parse the <title> tag out of a given URL"""
    d = getPage(url)

    d.addCallback(_parse_pagetitle, url)

    return d

def _parse_pagetitle(page_contents, url):
    pagetree = lxml.html.fromstring(page_contents)

    title = u" ".join(pagetree.xpath("//title/text()")).strip()
    title = title.encode("utf-8")

    if not len(title):
        title = "No title found"

    return "%s -- %s." % (url, title)

### ELO ###
def command_elo(rest):
    elo_finders = {u"lol": _get_lol_elo,
                   u"sc2": _get_sc2_elo,
                   u"dota2": _get_dota2_elo}

    typ, _, rest = rest.partition(" ")

    if typ == "help":
        return _get_help_elo()

    if typ in elo_finders:
        return elo_finders[typ](rest)

    raise NotImplementedError

def _get_help_elo():
    return "Usage: !elo {dota2,lol,sc2} nickname"

# TODO
def _get_sc2_elo(nickname, domain="eu"):
    return "Not implemented yet."

# TODO
def _get_dota2_elo(nickname, domain="eu"):
    return "Not implemented yet."

# TODO implement domain-specific search
def _get_lol_elo(nickname, domain="euw"):

    url = "http://competitive.%s.leagueoflegends.com/ladders/%s/current/rankedsolo5x5?summoner_name=%s" % (domain, domain, nickname)

    d = getPage(url)

    d.addCallback(_parse_lol_elo, nickname, domain)

    return d
 
   
def _parse_lol_elo(page_contents, nickname, domain):
    pagetree = lxml.html.fromstring(page_contents)

    elo = u" ".join(pagetree.xpath("//td[@class='views-field views-field-rating views-align-center']/text()")).strip()
    elo = elo.encode("utf-8")

    if not len(elo):
        elo = "No ELO found"

    return "%s (%s) -- %s." % (nickname, domain, elo) 

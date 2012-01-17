#!/usr/bin/env python
from twisted.web.client import getPage

import lxml.html
import random

"""Commands container, to be replaced with a plugin way of dealing with things
later on the lifecycle of scibby the irc bot!"""

### Default responses ###
def say_hi():
    return "Hi!"

### URL commands ###
def command_title(url):
    """Use lxml to parse the <title> tag out of a given URL"""
    d = getPage(url)

    d.addCallback(_parse_pagetitle, url)

    return d

def _parse_pagetitle(page_contents, url):
    pagetree = lxml.html.fromstring(page_contents)

    title = u"".join(pagetree.xpath("//title/text()")).strip()
    title = title.encode("utf-8")

    if not len(title):
        title = "No title found"

    return "%s -- %s." % (url, title)

### BROCODE ###
broquotes = ["As soon as we saw the fake boo, we had to get them outta here, because this is Grenade Free Zone.",
             "I'm like yea, we share girls why can't we share underwear?",
             "Baylife!",
             "I got spray tan on my nails and shit.",
             "We're going to get mini pedis. Vinny - You know, guy stuff",
             "I am the Angelina Jolie of incredible hot guys",
             "You cannot spell game without ME!",
             "Discouraging pre-marital sex is against my religion."]

def command_brolife(rest):
    return "BROLIFE!"

def command_baylife(rest):
    return "BAYLIFE BRO!"

def command_bro(rest):
    return "SUP BRAH?!"

def command_broquote(rest):
    return random.choice(broquotes)

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

    elo = u"".join(pagetree.xpath("//td[@class='views-field views-field-rating views-align-center']/text()")[0]).strip()
    elo = elo.encode("utf-8")

    if not len(elo):
        elo = "No ELO found"

    return "%s (%s) -- %s." % (nickname, domain, elo) 

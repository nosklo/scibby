#!/usr/bin/env python
from twisted.web.client import getPage

import lxml.html

"""Commands container, to be replaced with a plugin way of dealing with things
later on the lifecycle of scibby the irc bot!"""

def command_title(url):
    """Use lxml to parse the <title> tag out of a given URL"""
    d = getPage(url)

    d.addCallback(_parse_pagetitle, url)

    return d

def _parse_pagetitle(page_contents, url):
    pagetree = lxml.html.fromstring(page_contents)

    title = u" ".join(pagetree.xpath("//title/text()")).strip()
    title = title.encode("utf-8")

    return "%s -- %s" % (url, title)

def command_lolelo(nickname, domain="euw"):
    print "Getting LoL ELO for %s on %s" % (nickname, domain)
    url = "http://competitive.%s.leagueoflegends.com/ladders/%s/current/rankedsolo5x5?summoner_name=%s" % (domain, domain, nickname)

    d = getPage(url)

    d.addCallback(_parse_lolelo, nickname, domain)

    return d
    
def _parse_lolelo(page_contents, nickname, domain):
    pagetree = lxml.html.fromstring(page_contents)

    elo = u" ".join(pagetree.xpath("//td[@class='views-field views-field-rating views-align-center']/text()")).strip()
    elo = elo.encode("utf-8")

    print elo

    return "%s (%s) -- %s" % (nickname, domain, elo) 

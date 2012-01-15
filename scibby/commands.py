#!/usr/bin/env python
from twisted.web.client import getPage

import lxml.html

"""Commands container, to be replaced with a plugin way of dealing with things
later on the lifecycle of scibby the irc bot!"""

def command_title(self, url):
    """Use lxml to parse the <title> tag out of a given URL"""
    d = getPage(url)

    d.addCallback(_parse_pagetitle, url)

def _parse_pagetitle(self, page_contents, url):
    pagetree = lxml.html.fromstring(page_contents)

    title = u" ".join(pagetree.xpath("//title/text()")).strip()
    title = title.encode("utf-8")

    return "%s -- %s" % (url, title)

def command_lolelo(self, nickname, domain="euw"):
    url = "http://competitive.%s.leagueoflegends.com/ladders/%s/current/rankedsolo5x5?summoner_name=%s" % (domain, domain, nickname)
    
def _parse_lolelo(self, page_contents, url, nickname):
    pagetree = lxml.html.fromstring(page_contents)

    elo = u" ".join(pagetree.xpath("//td[@class='views-field-rating']/text()")).strip()

    return "%s -- %s" % (nickname, elo) 

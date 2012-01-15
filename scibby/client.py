#!/usr/bin/env python
import sys

from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service

from scibby import commands

HOST = "irc.quakenet.org"
PORT = 6667

class ScibbyClient(irc.IRCClient):
    nickname = "scibby"

    def signedOn(self):
        for channel in self.factory.channels:
            self.join(channel)

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition("!")

        message = message.strip()

        if not message.startswith("!"):
            return

        command, sep, rest = message.lstrip("!").partition(" ")

        func = getattr(commands, "command_" + command, None)

        if func is None:
            return

        d = defer.maybeDeferred(func, rest)
        # d.addErrback(self._show_error)

        if channel == self.nickname:
            d.addCallback(self._send_message, nick)
        else:
            d.addCallback(self._send_message, channel, nick)

    def _send_message(self, msg, target, nick=None):
        if nick:
            msg = "%s, %s" % (nick, msg)
        self.msg(target, msg)

    def _show_error(self, failure):
        return failure.getErrorMessage()

    def command_ping(self, rest):
        return "Pong."

class ScibbyFactory(protocol.ReconnectingClientFactory):
    protocol = ScibbyClient 
    channels = ["#scibbytest"]

if __name__ == "__main__":
    reactor.connectTCP(HOST, PORT, ScibbyFactory())
    log.startLogging(sys.stdout)
    reactor.run()
elif __name__ == "__builtin__":
    application = service.Application("scib")
    irc_service = internet.TCPClient(HOST, PORT, ScibbyFactory())
    irc_service.setServiceParent(application)

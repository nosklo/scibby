#!/usr/bin/env python
import sys

from twisted.internet import reactor, task, defer, protocol
from twisted.python import log
from twisted.words.protocols import irc
from twisted.application import internet, service

from scibby import commands
from scibby import pnp 
from scibby.config import values as configuration

class ScibbyClient(irc.IRCClient):
    nickname = configuration.nickname

    def signedOn(self):
        for channel in configuration.channels:
            self.join(channel)

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition("!")

        message = message.strip()

        if not message.startswith("!"):
            return

        if message.startswith("!"):
            """We received a command. This is either in the default scibby 
            commands or in one of the plugins."""

            command, sep, rest = message.lstrip("!").partition(" ")

            if command in commands.whitelist.keys():
                func = getattr(commands, command, None)
            else:
                # the func might be in one of the plugins, delegate to scibby.plugins
                if command in pnp.plugins:
	            func = pnp.plugins[command]._handler
                else:
                    func = None

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

def main():
    reactor.connectTCP(configuration.host, configuration.port, ScibbyFactory())
    log.startLogging(sys.stdout)
    reactor.run()

if __name__ == "__main__":
    main()
elif __name__ == "__builtin__":
    application = service.Application("scib")
    irc_service = internet.TCPClient(configuration.host, configuration.port, ScibbyFactory())
    irc_service.setServiceParent(application)

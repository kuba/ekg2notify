#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple (remote) notification plugin for ekg2.

"""

import os
import re

import ekg

# The path to fifo
home_dir = os.getenv('HOME')
fifo_dir = '%s/notify' % home_dir
ekg.variable_add('notify:fifo', fifo_dir)

# Sessions that should be tracked, separated by whitespace
ekg.variable_add('notify:sessions', '')

# Words that should be treaded as highlighted
# during MUCs (Multi User Chats), whitespace-separated.
# Only highlighted messages will be sent as notification.
ekg.variable_add('notify:highlights', '')

class Notify(object):
    """
    Handles sending notifications.

    :ivar ekgconfig: ekg2's config (ekg.config)
    :type ekgconfig: :class:`dict`

    """
    def __init__(self, config):
        """
        Initialize the notification system.

        Opens a FIFO (named pipe) and registers handlers.

        :param config: ekg2's config (ekg.config)
        :type config: :class:`dict`

        """
        self.ekgconfig = config

        fifo = self.ekgconfig['notify:fifo']
        ekg.echo("Opening pipe at %s!" % fifo)
        self.pipe = open(fifo, 'w+')

        ekg.handler_bind('protocol-message-received', self.message_handler)
        ekg.command_bind('notify-test', self.test_handler)

    def get_highlights(self):
        """
        Retireve watched highlights from config.

        """
        raw = self.ekgconfig['notify:highlights']
        return raw.split()

    def get_sessions(self):
        """
        Retrieve watched sessions from config.

        """
        raw = self.ekgconfig['notify:sessions']
        names = raw.split()
        sessions = {}
        for name in names:
            try:
                session = ekg.session_get(name)
            except KeyError:
                ekg.echo("Session '%s' doesn't exist" % name)
            else:
                sessions[name] = session
        return sessions

    def _send(self, msg):
        """
        Write to pipe.

        """
        self.pipe.write(msg + '\n')
        self.pipe.flush()

    def send(self, nickname, msg):
        """
        Sends a notification.

        Notification is sent in format: nickname\tmsg

        :param nickname: Nickname of the sender
        :type nickname: :class:`str`

        :param msg: Message sent by the sender
        :type msg: :class:`str`

        """
        msg = '%s\t%s' % (nickname, msg)
        self._send(msg)

    def filter_entities(self, text):
        text = re.sub('&', '&amp;', text)
        text = re.sub('<', '&lt;', text)
        text = re.sub('>', '&gt;', text)
        text = re.sub('\n', ' ', text)
        return text

    def test_handler(self, name, args):
        """
        Send test notification.

        """
        self.send("Test notify!", self.filter_entities(args))

    def message_handler(self, session_name, uid, type, text, sent_time, ignore_level):
        """
        Send message notification if from watched session.

        """
        sessions = self.get_sessions()

        # Is the session watched?
        if sessions.has_key(session_name):
            session = sessions[session_name]

            # Clear all special ANSI control characters (like colors) from message
            text = re.sub(r'(\x1b\[.*?m)|\xc2\xa0', '', text)

            try:
                sender, message = re.search(r'[<\(](.*?)[>\)]\s*(.*)\s*$', text).groups()
            except AttributeError:
                # Private message
                try:
                    user = session.user_get(uid)
                except KeyError:
                    sender = uid
                else:
                    sender = user.nickname
                message = text
            else:
                # MUC-like message
                # We want only highlighted messages
                if not re.search('|'.join(self.get_highlights()), text):
                    # Fix IRC
                    if session_name.startswith('irc:'):
                        if "#" in uid:
                            return
                    else:
                        return

            self.send(sender, self.filter_entities(message))
        

notify = Notify(ekg.config)

def init():
    if len(ekg.config['notify:sessions']) == 0:
        ekg.echo(
            """
            It seems to be the first time using Ekg2Notify, hm? ;)
            Start off by adding watched sessions (space separated),
            eg.: /set notify:sessions xmpp:example@example.com irc:freenode
        
            When using MUC (Multi User Chat), only some messages are sent,
            ie. those contaning predefined words - "highlights".
            Add them (space separated) by /set notify:highlights
        
            You can also change the default FIFO location (/set notify:fifo),
            though remember to reload the script afterwards.")
        
            Have fun! ;D"""
            )

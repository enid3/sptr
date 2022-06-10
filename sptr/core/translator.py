from tkinter.ttk import Notebook

from sptr.commands.command import CommandContainer
from sptr.core import settings
import threading
import queue

from sptr.core.actions import Actions
from sptr.core.share import TranslatorAware
from sptr.dictionary.googletrans import GoogleDict
from sptr.dictionary.manager import DictionaryManager
from tkinter import *

import pwd
import os

from sptr.ext.communication_handler import RemoteConsoleHandler
from sptr.ui.gui import UI

import logging

class Translator(Actions):
    LOG = logging.getLogger(__name__)
    title = 'sptr'
    def __init__(self, settings):
        TranslatorAware.tr_set(self)
        self.settings = settings
        self.msg = "asdfasfasfasf"
        self.q = queue.Queue()
        self.dm = DictionaryManager()
        self.commands = CommandContainer()
        self.ui = UI(Translator.title)
        self.rch = None

        self.notebook = Notebook()
        try:
            self.username = pwd.getpwuid(os.geteuid()).pw_name
        except KeyError:
            self.username = 'uid:' + str(os.geteuid())

    def initialize(self):
        self.ui.initialize()
        if self.settings.config:
            self.configure(self.settings.config)

    def set_option_from_string(self, name, value):
        self.settings.set(name, value)

    def get_console_address(self):
        return 'localhost', self.settings.remote_console_port

    def notify(self, msg):
        self.msg = msg
        print(msg)
        print(self.q)
        print(f'putting {msg}')
        self.q.put(msg)
        print(f'{self.q.qsize()} {self.q.empty()} ')

    def destroy(self):
        if self.ui:
            self.ui.destroy()

        if self.dm:
            self.dm.destroy()



import tkinter as tk
from multiprocessing.connection import Client
from tkinter import *

from sptr.core.share import TranslatorAware
from sptr.ui.widgets.console import Console

from sptr.ui.widgets.chooser import Chooser
from sptr.ui.widgets.representer import Representer


class UI(tk.Tk, TranslatorAware):
    def __init__(self, title):
        tk.Tk.__init__(self)
        self.title(title)

        self.chooser = Chooser(self)
        self.representer = Representer(self)
        self.console = Console(self)

    def initialize(self):
        #self.title("sptr")

        self.chooser.initialize()
        #self.representer.initialize()
        self.console.initialize()

        self.chooser.pack(fill=BOTH)
        self.representer.pack(fill=BOTH, expand=True)

        self.console.pack(side=BOTTOM, fill=X)

        self.init_basic_binds()

    def on_exit(self, event=None):
        print('on exit')
        with Client(self.tr.rch.address) as conn:
            print('sending exit')
            conn.send('exit')
        self.destroy()

    def init_basic_binds(self):
        self.chooser.listbox.bind("<<ListboxSelect>>",
                                  lambda x: self.tr._translate(
                                      self.chooser.get()))

        self.protocol('WM_DELETE_WINDOW', self.on_exit)



    def popup(self, s):
        from tkinter import messagebox
        messagebox.showinfo("notify", s)
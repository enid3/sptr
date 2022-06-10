from sptr.core.share import TranslatorAware
from sptr.commands.command import Command
import tkinter as tk


# TODO save history to file
class Console(TranslatorAware, tk.Entry):
    history = None
    prompt = ':'

    def __init__(self, master):
        super(Console, self).__init__(master)
        # self.history = History(self.tr.settings.max_console_history_length, 100)
        self.pos = 0
        self.line = ''

    def initialize(self):
        self.bind("<Return>",
                  lambda x: self.handle())
        self.bind("<Escape>",
                  lambda x: self.master.focus_set())
        pass

    def clear(self):
        self.pos = 0
        self.line = ''

    def get_cmd_class(self):
        return self.tr.commands.get_command(self.line.split()[0], abbrev=True)

    def _get_cmd(self) -> Command:
        try:
            cmd_cls = self.get_cmd_class()
            print(cmd_cls)
        except Exception:
            return None

        print(f'arg: {self.line}')
        return cmd_cls(self.line)

    def close(self):
        cmd = self._get_cmd()
        if cmd:
            cmd.cancel()
        self.clear()

    def execute(self, cmd=None):
        if cmd == None:
            cmd = self._get_cmd()
            print(cmd)
        if cmd:
            cmd.execute()
            # self.history.add(self.line)
            #self.close()

    def handle(self):
        prompt = self.get()[0]
        self.line = self.get()[1:]
        if prompt == ':':
            self.execute()
        elif prompt == '/':
            self.tr.search(self.line)

    def pres(self):
        pass

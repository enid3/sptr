from tkinter import *


class Chooser(Frame):
    def __init__(self, master):
        super(Chooser, self).__init__(master)

        self.scrollbar = Scrollbar(self, orient=VERTICAL)
        self.listbox = Listbox(self, selectmode=SINGLE)

    def initialize(self):
        #self.pack(fill=Y, expand=True, anchor=NW)
        self.listbox.pack(fill=Y, side=LEFT)

        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.pack(side=LEFT, fill=BOTH, expand=True)

    def clear(self):
        self.listbox.delete(0, END)

    def add(self, s: str):
        self.listbox.insert(0, s)

    def get(self):
        sel = self.listbox.curselection()
        if sel:
            return self.listbox.get(sel[0])
        return  None

    def index_next(self):
        sel = self.listbox.curselection()
        next_index = None
        if sel:
            next_index = min(sel[0] + 1, self.listbox.size() - 1)
        else:
            if self.listbox.size():
                next_index = 0
        if next_index is not None:
            self.listbox.select_clear(0, END)
            self.listbox.select_set(next_index)
            if next_index != self.listbox.size():
                self.listbox.yview_scroll(1, 'units')
            else:
                self.listbox.yview(END)

        return next_index

    def index_prev(self):
        sel = self.listbox.curselection()
        prev_index = None
        if sel:
            prev_index = max(sel[0] - 1, 0)
        else:
            if self.listbox.size():
                prev_index = 0

        if prev_index is not None:
            self.listbox.select_clear(0, END)
            self.listbox.select_set(prev_index)
            if prev_index != 0:
                self.listbox.yview_scroll(-1, 'units')
            else:
                self.listbox.yview(0)

        return prev_index

    def select_index(self, index: int):
        return
        if index is not None:
            self.listbox.select_clear(0, END)
            self.listbox.select_set(index)
            self.listbox.yview_scroll(1, 'units')

    def next_page(self):
        self.listbox.yview_scroll(1, 'pages')

    def prev_page(self):
        self.listbox.yview_scroll(-1, 'pages')

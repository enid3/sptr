from tkinter import *
from tkinter.ttk import Notebook

import sptr.dictionary.translated
from sptr.ui.widgets.translatedframe import TranslatedFrame


class Representer(Notebook):
    def __init__(self, master):
        super(Representer, self).__init__(master)
        self.translatedFrames = []

    def fill(self, translations: []):
        for item in self.winfo_children():
            item.destroy()

        self.translatedFrames.clear()

        if translations:
            for tr in translations:
                frame = TranslatedFrame(self)
                frame.represent(tr)
                frame.pack(fill=BOTH, expand=True)
                self.translatedFrames.append(frame)

                if tr.dictionary:
                    self.add(frame, text=tr.dictionary.name)
                else:
                    self.add(frame, text='unknown dict')
        self.pack()

    def next_dict(self):
        next_id = min(self.index(self.select()) + 1, len(self.tabs()) - 1)
        self.select(next_id)

    def prev_dict(self):
        prev_id = max(self.index(self.select()) - 1, 0)
        self.select(prev_id)

    def get_selected_translated(self):
        id = self.index(self.select())
        return self.translatedFrames[id].get_translated()

if __name__ == '__main__':
    tk = Tk()
    tk.title('sptr')
    r = Representer(tk)
    l = [
        sptr.dictionary.translated.example,
        sptr.dictionary.translated.example,
        sptr.dictionary.translated.example,
        sptr.dictionary.translated.example,
        sptr.dictionary.translated.example,
    ]
    r.fill(l)
    tk.mainloop()
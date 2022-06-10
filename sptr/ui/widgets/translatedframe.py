from tkinter import *

import sptr.dictionary.translated
from sptr.dictionary.translated import Translated


class TranslatedFrame(Frame):
    def __init__(self, master):
        super(TranslatedFrame, self).__init__(master)

        self.translated = None

        # origin
        self.origin_frame = Frame(self)
        self.origin_label = Label(self.origin_frame, font='Helvetica 11')
        self.clarification_label = Label(self.origin_frame,
                                         font='Helvetica 11 bold')
        self.dictionary_label = Label(self.origin_frame,
                                      font='Helvetica 11 italic', relief=GROOVE)
        self.definition_message = Message(self.origin_frame, width=450)

        # type
        self.type_frames = []

        # specification
        self.specification_frames = []

    def fill_origin_frame(self, tr: Translated):
        # origin_label
        self.origin_label.configure(text=tr.origin)
        self.origin_label.pack(side=LEFT, anchor=NW)

        # clarification_label
        if tr.clarification:
            self.clarification_label.configure(text=f'[{tr.clarification}]')
        else:
            self.clarification_label.configure(text='')
        self.clarification_label.pack(side=LEFT, anchor=NW)

        # dictionary_label
        self.dictionary_label.configure(text=tr.dictionary.name)
        self.dictionary_label.pack(side=RIGHT, anchor=NE)

        # definition_message
        self.definition_message.configure(text=tr.definition)
        self.definition_message.pack(side=BOTTOM, anchor=S)

        self.origin_frame.pack(side=TOP, fill=BOTH)

    def fill_type_frames(self, tr: Translated):
        prefix = '-'
        # clear
        for type_frame in self.type_frames:
            type_frame.destroy()
        self.type_frames.clear()

        # fill
        for type_name, descriptions in tr.types.items():
            type_frame = LabelFrame(self, text=type_name)
            for d in descriptions:
                label = Message(type_frame, text=prefix + d, width=450)
                label.pack(anchor=W)

            type_frame.pack(side=TOP, fill=BOTH)
            self.type_frames.append(type_frame)

    def fill_specification_frames(self, tr: Translated):
        # clear
        for spec_frame in self.specification_frames:
            spec_frame.destroy()
        self.specification_frames.clear()

        # fill
        for spec_name, specification in tr.specifications.items():
            spec_frame = Frame(self)
            spec_frame.pack(side=TOP, fill=BOTH)
            name_label = Label(spec_frame, text=f'{spec_name}:',
                               font='Helvetica 10 bold')
            name_label.pack(anchor=NW)

            for s in specification:
                data_label = Message(spec_frame, text=s, width=450)
                data_label.pack(anchor=W)

            spec_frame.pack(side=TOP, fill=BOTH)
            self.specification_frames.append(spec_frame)

    def represent(self, tr: Translated):
        self.translated = tr
        self.fill_origin_frame(tr)
        self.fill_type_frames(tr)
        self.fill_specification_frames(tr)
        self.pack(fill=BOTH, expand=True)

    def get_translated(self):
        return self.translated


if __name__ == '__main__':
    tk = Tk()
    tk.title('sptr')
    tf = TranslatedFrame(tk)
    tf.represent(sptr.dictionary.translated.example)
    tf.represent(sptr.dictionary.translated.example)
    tf.represent(sptr.dictionary.translated.example)
    tk.mainloop()

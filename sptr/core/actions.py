from sptr.core.share import TranslatorAware, SettingsAware


class Actions(TranslatorAware, SettingsAware):
    def notify(self, *args):
        self.tr.ui.popup(' '.join(args))

    def execute(self, command: str):
        try:
            print(command.split()[0])
            cmd_cls = self.tr.commands.get_command(command.split()[0], abbrev=True)
        except Exception:
            print("exception")
        cmd = cmd_cls(command)
        print(cmd)
        print(cmd.line)
        print('before executing')
        cmd.execute()
        print('after executing')

    def search(self, word: str):
        res = self.tr.dm.get(word)

        chooser = self.tr.ui.chooser
        chooser.clear()

        for word in res:
            chooser.add(word)

        #lb.select_set(0)
        #self.fill_notebook(nb, lb.get(lb.curselection()[0]))

    def _translate(self, word: str):
        translations = self.tr.dm.translate(word)
        self.tr.ui.representer.fill(translations)

    def bind(self, key, *args):
        command = ' '.join(args)

        def command_warper(event=None):
            if event:
                if event.widget != self.tr.ui.console:
                    self.execute(command)

        self.tr.ui.bind(key, command_warper)

    def configure(self, conf):
        if not conf:
            self.tr.LOG.info('no config file specified')
            return

        with open(conf) as conf_file:
            self.tr.LOG.info(f'reading config file from {conf}')

            commands = conf_file.readlines()
            for command in commands:
                command = ' '.join(command.split())
                if command.startswith('#'):
                    continue
                if command:
                    self.tr.execute(command)

        self.tr.LOG.info('no config file specified')

    def show(self):
        self.tr.ui.update()
        self.tr.ui.deiconify()

    def hide(self):
        self.tr.ui.update()
        self.tr.ui.withdraw()

    def move_next(self):
        index = self.tr.ui.chooser.index_next()
        print(index)
        self.select(index)

    def move_prev(self):
        index = self.tr.ui.chooser.index_prev()
        self.select(index)

    def select(self, index):
        self.tr.ui.chooser.select_index(index)
        self.tr._translate(self.tr.ui.chooser.get())

    def page_next(self):
        self.tr.ui.chooser.next_page()

    def page_prev(self):
        self.tr.ui.chooser.prev_page()

    def next_dict(self):
        self.tr.ui.representer.next_dict()

    def prev_dict(self):
        self.tr.ui.representer.prev_dict()

    def fav(self):
        translated = self.tr.ui.representer.get_selected_translated()
        self.tr.dm.favourite.write(translated)

    def change_lang(self, lang):
        self.tr.dm.change_lang(lang)
        self.tr.ui.chooser.clear()

    def load_dict(self, *args):
        self.tr.dm.load_dict(*args)
        #print(self.tr.dm.all_dictionaries)
        #print(elf.tr.dm.ac)

    def load_dict_type(self, *args):
        #self.tr.dm.load_dict_type(args)
        pass



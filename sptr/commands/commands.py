from sptr.commands.command import Command


class quit(Command):

    def execute(self):
        import sys
        sys.exit(0)
        # self.tr.exit()

class echo(Command):
    def execute(self):
        print(self.rest(1))


class translate(Command):
    def execute(self):
        translations = self.tr.dm.safe_translate(self.rest(1))
        self.tr.ui.representer.fill(translations)

class speech(Command):
    def execute(self):
        pass
        translations = self.tr.dm.safe_translate(self.rest(1))
        #self.tr.ui.representer.fill(translations)


class set_(Command):
    name = 'set'

    def execute(self):
        name, value, _ = self.parse_setting_line()
        self.log.info(f'{name}:{value}')
        self.tr.set_option_from_string(name, value)


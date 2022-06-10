from sptr.core.share import TranslatorAware
from sptr.ext.lazy_property import lazy_property

import re

_SETTINGS_RE = re.compile(r'^\s*([^\s]+?)=(.*)$')


class CommandContainer(TranslatorAware):

    def __init__(self):
        self.commands = dict()

    def __getitem__(self, key):
        return self.commands[key]

    def load_commands_from_module(self, module):
        for var in vars(module).values():
            try:
                if issubclass(var, Command) and var != Command:
                    # print(f"Loading command: {var.__name__}")
                    self.commands[var.get_name()] = var  # _command_init(var)
            except TypeError:
                pass

    def load_commands_from_object(self, obj, filtr, ent):
        print(filtr)
        for attribute_name in dir(obj):
            # print("attribute name: " + attribute_name)
            if attribute_name[0] == '_' or attribute_name in filtr:
                continue
            attribute = getattr(obj, attribute_name)
            # print("attribute: " + attribute)
            if hasattr(attribute, '__call__'):
                print("adding: " + attribute_name)
                self.commands[attribute_name] = command_function_factory(
                    attribute, ent)

    def get_command(self, name, abbrev=False):
        if abbrev:
            lst = [cls for cmd, cls in self.commands.items()
                   if cls.allow_abbrev and cmd.startswith(name) or cmd == name]
            if not lst:
                raise KeyError
            if len(lst) == 1:
                return lst[0]
            try:
                if self.commands[name] in lst:
                    return self.commands[name]
            finally:
                raise ValueError("Ambiguous command")

        try:
            return self.commands[name]
        except KeyError:
            return None

    def command_generator(self, start):
        return sorted(
            cmd + ' ' for cmd in self.commands if cmd.startswith(start))


class Command(TranslatorAware):
    """Abstract command class"""
    name = None
    allow_abbrev = True
    quantifier = None
    _shifted = 0
    _setting_line = None

    def __init__(self, line, quantifier=None):
        self.init_line(line)
        self.quantifier = quantifier

    def init_line(self, line):
        self.line = line
        self.args = line.split()
        try:
            self.firstpart = line[:line.rindex(' ') + 1]
        except ValueError:
            self.firstpart = ''

    @classmethod
    def get_name(cls):
        classdict = cls.__mro__[0].__dict__
        if 'name' in classdict and classdict['name']:
            return cls.name
        return cls.__name__

    def execute(self):
        """Called when command executed"""

    def tab(self, tabnum):
        """called on <TAB> press"""

    def quick(self):
        """Called after each keypress"""

    def cancel(self):
        """On console closed"""

    # Easy ways to get information
    def arg(self, n):
        """Returns the nth space separated word"""
        try:
            return self.args[n]
        except IndexError:
            return ""

    def rest(self, n):
        """Returns everything from and after arg(n)"""
        got_space = True
        word_count = 0
        for i, char in enumerate(self.line):
            if char.isspace():
                if not got_space:
                    got_space = True
                    word_count += 1
            elif got_space:
                got_space = False
                if word_count == n + self._shifted:
                    return self.line[i:]
        return ""

    def start(self, n):
        """Returns everything until (inclusively) arg(n)"""
        return ' '.join(self.args[:n]) + " "  # XXX

    def shift(self):
        del self.args[0]
        self._setting_line = None
        self._shifted += 1

    def parse_setting_line(self):
        """
        Parses the command line argument that is passed to the `:set` command.
        Returns [option, value, name_complete].

        Can parse incomplete lines too, and `name_complete` is a boolean
        indicating whether the option name looks like it's completed or
        unfinished.  This is useful for generating tab completions.

        >>> Command("set foo=bar").parse_setting_line()
        ['foo', 'bar', True]
        >>> Command("set foo").parse_setting_line()
        ['foo', '', False]
        >>> Command("set foo=").parse_setting_line()
        ['foo', '', True]
        >>> Command("set foo ").parse_setting_line()
        ['foo', '', True]
        >>> Command("set myoption myvalue").parse_setting_line()
        ['myoption', 'myvalue', True]
        >>> Command("set").parse_setting_line()
        ['', '', False]
        """
        if self._setting_line is not None:
            return self._setting_line
        match = _SETTINGS_RE.match(self.rest(1))
        if match:
            self.firstpart += match.group(1) + '='
            result = [match.group(1), match.group(2), True]
        else:
            result = [self.arg(1), self.rest(2), ' ' in self.rest(1)]
        self._setting_line = result
        return result

    def parse_flags(self):
        """Finds and returns flags in the command

        >>> Command("").parse_flags()
        ('', '')
        >>> Command("foo").parse_flags()
        ('', '')
        >>> Command("shell test").parse_flags()
        ('', 'test')
        >>> Command("shell -t ls -l").parse_flags()
        ('t', 'ls -l')
        >>> Command("shell -f -- -q test").parse_flags()
        ('f', '-q test')
        >>> Command("shell -foo -bar rest of the command").parse_flags()
        ('foobar', 'rest of the command')
        """
        flags = ""
        args = self.line.split()
        rest = ""
        if args:
            rest = self.line[len(args[0]):].lstrip()
            for arg in args[1:]:
                if arg == "--":
                    rest = rest[2:].lstrip()
                    break
                elif len(arg) > 1 and arg[0] == "-":
                    rest = rest[len(arg):].lstrip()
                    flags += arg[1:]
                else:
                    break
        return flags, rest

    @lazy_property
    def log(self):
        import logging
        return logging.getLogger('commands.' + self.__class__.__name__)


def command_function_factory(func, obj):
    class CommandFunction(Command):
        __doc__ = func.__doc__

        def execute(self):  # pylint: disable=too-many-branches
            if not func:
                print(f'None')
                return None
            if len(self.args) == 1:
                print(f'len == 1')
                try:
                    return func(**{'narg': self.quantifier})
                except TypeError:
                    if obj:
                        return func(obj)
                    else:
                        return func()

            args, kwargs = list(), dict()
            if obj:
                args.append(obj)
            for arg in self.args[1:]:
                print(f'arg: {arg}')
                equal_sign = arg.find("=")
                value = arg if equal_sign == -1 else arg[equal_sign + 1:]
                try:
                    value = int(value)
                except ValueError:
                    if value in ('True', 'False'):
                        value = (value == 'True')
                    else:
                        try:
                            value = float(value)
                        except ValueError:
                            pass

                if equal_sign == -1:
                    args.append(value)
                else:
                    kwargs[arg[:equal_sign]] = value

            if self.quantifier is not None:
                kwargs['narg'] = self.quantifier

            try:
                if self.quantifier is None:
                    print(f'func: {args} {kwargs}')
                    return func(*args, **kwargs)
                else:
                    try:
                        return func(*args, **kwargs)
                    except TypeError:
                        del kwargs['narg']
                        return func(*args, **kwargs)
            except TypeError:
                raise

    CommandFunction.__name__ = func.__name__
    return CommandFunction

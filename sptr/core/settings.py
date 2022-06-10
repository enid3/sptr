from sptr.core.share import TranslatorAware

ALLOWED_SETTINGS = {
    'remote_console_port': int,
    'lang_destination': str,
    'max_console_history_length': int,
    'stdin': bool,
    'server': bool,
    'config': str,
    'favourite_path': str,
}

ALLOWED_VALUES = {
    'test': (True, False),
    'str': ('str1', 'str2')

}

DEFAULT_VALUES = {
    bool: False,
    type(None): None,
    str: "",
    int: 0,
    float: 0.0,
    list: [],
    tuple: tuple([]),
}

PREDETERMINED_VALUES = {
    'remote_console_port': 5127,
    'lang_destination': 'ru',
    'favourite_path': '/home/hd/.sptr_favourite',
}


class Settings(TranslatorAware):
    def __init__(self):
        self._settings = dict()

    @staticmethod
    def _check_type(name, value):
        return isinstance(value, ALLOWED_SETTINGS[name])

    def set(self, name, value):
        assert name in ALLOWED_SETTINGS, f'Setting {name} not found.'
        #if name not in self._settings:
        self._settings[name] = value
        assert self._check_type(name, value), \
            f'Wrong type of {value} for {name},' \
            f' {ALLOWED_SETTINGS[name]} required'

        #raise NotImplemented

    @staticmethod
    def _get_default(name):
        if name in PREDETERMINED_VALUES:
            value = PREDETERMINED_VALUES[name]
        else:
            value = DEFAULT_VALUES[ALLOWED_SETTINGS[name]]

        return value

    def get(self, name):
        assert name in ALLOWED_SETTINGS, f'Setting {name} not found.'
        if name in self._settings:
            value = self._settings[name]
        else:
            value = self._get_default(name)

        return value

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self.set(name, value)

    def __getattr__(self, name):
        if name.startswith('_'):
            return self._settings[name]
        else:
            return self.get(name)

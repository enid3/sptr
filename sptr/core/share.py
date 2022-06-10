class TranslatorAware:
    tr = None
    """Give access to global Translator object"""
    @staticmethod
    def tr_set(tr):
        TranslatorAware.tr = tr


class SettingsAware:
    @staticmethod
    def settings_set(settings):
        SettingsAware.settings = settings

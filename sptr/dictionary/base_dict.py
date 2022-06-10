from sptr.core.share import SettingsAware


class BaseDictionary(SettingsAware):
    typename = ''

    def __init__(self):
        self.name = ''
        self.description = ''
        self.to_be_cached = True
        self.max_cache_size = 2048
        self.word_count = 0

    def get(self, regexp: str) -> []:
        """
        Used by DictionaryManager, to get list of suggested words, satisfying
        regexp, that might be translated by this dictionary.
        """
        return None

    def translate(self, word: str):
        """
        Used by DictinaryManager to translate word;
        Guaranteed, that word was in list, returned by get method.
        """
        pass

    def get_supported_langs(self) -> []:
        """
        Used to generate list of supported languages, this list will
        be used to tab-complimenting only.
        Even if this method won't contain some language, method
        is_supported will be called anyway.
        """
        pass

    def is_lang_supported(self, lang: str) -> bool:
        """
        Method called by DictionaryManager, when new language specified,
        in case, it returns true, dictionary will be used, and, if false,
        will not and method ... will be called.
        """
        pass

    def load(self):
        """
        Called once, should be used instead of __init__ to recourse allocating;
        This method should load memory demanding data.
        Guaranteed that it was called before any kind of operation with dict.
        """
        pass

    def unload(self):
        """
        Called once, should be used recourse freeing;
        This method should unload memory demanding data.
        After this call, this dictionary won't be used.
        """
        pass

    def suspend(self):
        """
        Called, when new language specified and this dictionary method
        is_lang_supported returned false.
        Guaranteed that in case it was called before next usage of
         this dict, method resume will be called.
        """
        pass

    def resume(self):
        """
        Called, when new language specified and this dictionary method
        is_lang_supported returned true.
        Guaranteed that in case it was called before next usage of
        this dict, this method will be called.
        """
        pass


class BaseWritableDictionary(BaseDictionary):
    def write(self, translated):
        """
        Writes translated to dictionary.
        :param translated: object of Translated type to be written.
        """
        pass

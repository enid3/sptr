import os

import sptr.dictionary.base_dict
from sptr.core.share import TranslatorAware, SettingsAware


from sptr.dictionary.googletrans import GoogleDict
from sptr.dictionary.base_dict import BaseDictionary
from sptr.dictionary.stardict import Stardict


class DictionaryManager(TranslatorAware, SettingsAware):

    def __init__(self):
        self.dict_types = dict()
        self.all_dictionaries = list()
        self.active_dictionaries = list()
        self._lang = ''

        self.load_dict_type('dictionary', '/home/hd/dev/sptr/sptr/dictionary/stardict.py')
        self.load_dict_type('favourite', '/home/hd/dev/sptr/sptr/dictionary/favourite.py')
        # print(self.dict_types)
        #self.dictionaries.append(GoogleDict())
        dir = '/home/hd/mnt/dict'
        for subdirs, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith('.idx'):
                    pass
                    #self.load_dict('stardict', subdirs + os.sep + file[:-4], ("en-ru"))
                    # print('stardict ' + subdirs + os.sep + file[:-4])

        """
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-lingvo-ER-FinancialManagement-2.4.2/ER-FinancialManagement', ('en-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-dal-2.4.2/dal', ('ru-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-lingvo-ER-Wine-2.4.2/ER-Wine', ('en-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-lingvo-ER-Computers-2.4.2/ER-Computers', ('en-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-lingvo-ER-Physics-2.4.2/ER-Physics', ('en-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-brokg-2.4.2/brokg', ('en-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-lingvo-ER-GreatBritain-2.4.2/ER-GreatBritain', ('en-ru'))
        self.load_dict('stardict', '/home/hd/mnt/dict/stardict-lingvo-ER-Grammar-2.4.2/ER-LingvoGrammar', ('en-ru'))
        """
        self.favourite = self.load_dict('favourite')

        for d in self.all_dictionaries:
            d.load()

        self.change_lang('en-ru')

        self.res = {}
        self.prev_word = ''
        pass

    def load_dict_type(self, name: str, path: str):
        print('load dict type')
        def import_file(name, path):  # From https://stackoverflow.com/a/67692
            # pragma pylint: disable=no-name-in-module,import-error,no-member, deprecated-method
            import sys
            if sys.version_info >= (3, 5):
                import importlib.util as util
                spec = util.spec_from_file_location(name, path)
                module = util.module_from_spec(spec)
                spec.loader.exec_module(module)
            elif (3, 3) <= sys.version_info < (3, 5):
                from importlib.machinery import SourceFileLoader
                # pylint: disable=no-value-for-parameter
                module = SourceFileLoader(name, path).load_module()
            else:
                import imp
                module = imp.load_source(name, path)
            # pragma pylint: enable=no-name-in-module,import-error,no-member
            return module

        print(name)
        print(path)
        module = import_file(name, path)
        for var in vars(module).values():
            try:
                if issubclass(var, BaseDictionary) and var != BaseDictionary:
                    self.dict_types[var.typename] = var
            except TypeError:
                pass

    def load_dict(self, dict_type: str, *args, **kwargs):
        dictionary = self.dict_types[dict_type](*args, **kwargs)
        #if(dictionary.is)
        self.all_dictionaries.append(dictionary)
        if(dictionary.is_lang_supported(self._lang)):
            dictionary.resume()
            self.active_dictionaries.append(dictionary)
        print(f'{dictionary.name} loaded, {dictionary.word_count}')
        dictionary.load()
        return dictionary

    def get(self, word: str) -> {}:
        self.res = {}
        print('in get')
        print(f'word: {word}')
        print(self.active_dictionaries)
        for dictionary in self.active_dictionaries:
            words = dictionary.get(word)
            print(f'words: {words} form {dictionary.name}')
            for w in words:
                if not w:
                    continue

                if w in self.res:
                    self.res[w].append(dictionary)
                else:
                    self.res[w] = [dictionary]

        return self.res

    def change_lang(self, lang: str):
        if self._lang == lang:
            return

        old_active = self.active_dictionaries.copy()
        self.active_dictionaries.clear()

        # adding dictionaries
        #if not self._lang:
        for d in self.all_dictionaries:
            print(f'checking: {d.name}')
            if d.is_lang_supported(lang):
                print("lang supported")
                self.active_dictionaries.append(d)

        # suspend & resume
        for d in self.all_dictionaries:
            if d.is_lang_supported(lang):
                if d not in old_active:
                    d.resume()
            else:
                if d in old_active:
                    d.suspend()

        self._lang = lang
        print(self.active_dictionaries)

    def translate(self, word: str) -> []:
        if not word:
            return []

        dictionaries = self.res[word]
        translations = []
        for d in dictionaries:
            t = d.translate(word)
            t.dictionary = d
            translations.append(t)

        return translations

    def safe_translate(self, word: str):
        translations = []
        word = ''.join(word.split())
        for d in self.active_dictionaries:
            dget = d.get(word)
            if word in dget:
                t = d.translate(word)
                t.dictionary = d
                translations.append(t)

        return translations

    def clear(self):
        self.res = {}
        self.prev_word = ''

    def destroy(self):
        for d in self.all_dictionaries:
            d.unload()

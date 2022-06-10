from sptr.core.share import TranslatorAware
from sptr.dictionary.base_dict import BaseWritableDictionary

import re

class FavouriteDict(BaseWritableDictionary, TranslatorAware):
    typename = 'favourite'

    def __init__(self):
        self.name = 'favourite'
        self.description = 'Dictionary with added by user elements'
        self.words = {}
        self.word_count = 0

    def get(self, regexp: str):
        print('getting favourite')
        print(self.words)
        return [w for w in self.words if re.match(regexp, w)]

    def translate(self, word: str):
        return self.words[word]

    def get_supported_langs(self) -> []:
        return [self.typename]

    def is_lang_supported(self, lang: str) -> bool:
        import re
        print(lang)
        return re.match(lang, self.typename)


    def load(self):
        print('loading')
        self.file_name = self.tr.settings.favourite_path
        print(self.file_name)
        self.load_data()

    def save_data(self):
        """
        print('saving')
        import json
        print(self.words)
        print(self.file_name)
        f = open(self.file_name, 'w')

        f.write(str(self.words))
        print('here')
        #json.dump(self.words, f)
        # f.write(json.dumps(self.words))
        print('after with')
        """
        pass

    def load_data(self):
        """
        print('loading data')
        import json
        with open(self.file_name) as f:
            self.words = json.load(f)

        print(self.words)
        """
        pass

    def unload(self):
        print('unloading')
        self.save_data()

    def suspend(self):
        print('suspend')
        self.save_data()
        # self.words = {}

    def resume(self):
        print('resume')
        self.load_data()

    def write(self, translated):
        if translated:
            word = f'{translated.origin} [{translated.dictionary.name}]'
            # translated.dictionary = translated.dictionary.name
            self.words[word] = translated
            print('afterr:')
            print(self.words)
            self.save_data()


# This file is part of sptr, the dictionary application.
# License: GNU GPL version 3, see the file "AUTHORS" for details.

from googletrans import Translator

from sptr.dictionary.base_dict import BaseDictionary
from sptr.dictionary.translated import Translated


class GoogleDict(BaseDictionary):
    typename = 'googletrans'

    def __init__(self):
        super().__init__()
        self.name = "Google Translate"
        self.description = "Use google translate api to get translation"
        self._translator = Translator()
        self.word_count = 0

    def __getitem__(self, word, dest=None):
        if dest is None:
            dest = self.settings.lang_destination

        return self._translator.translate(word, dest=dest).text

    def translate(self, word: str) -> Translated:
        print("google dist ")
        dest = self.settings.lang_destination

        res = self._translator.translate(word, dest=dest)
        tr = Translated(word, '', res.pronunciation,
                        {
                            '': [res.text]
                        },
                        )
        return tr

    def get(self, word: str):
        return [word]

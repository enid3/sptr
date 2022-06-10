from pystardict import Dictionary

from sptr.dictionary.base_dict import BaseDictionary
from sptr.dictionary.translated import Translated
import re


class Stardict(BaseDictionary):
    typename = 'stardict'
    re_tags = re.compile(r'<.*?>')
    re_def = re.compile(r'<dtrn>.*</dtrn>')
    re_example = re.compile(r'<ex>.*</ex>')
    re_refs = re.compile(r'<kref>.*</kref>')

    def __init__(self, file_prefix: str, langs: ()):
        super().__init__()
        self._langs = langs
        self._dict = Dictionary(file_prefix)
        self._words = []
        self.name = self._dict.ifo.bookname
        self.description = self._dict.ifo.description
        self.word_count = self._dict.ifo.wordcount

        self._get_search_word = ''
        self._get_search_cache = []

    def translate(self, word: str) -> Translated:
        if word:
            import re
            tr = Translated(word)
            data = self._dict[word]

            defenition = [self.re_tags.sub('', w) for w in
                          re.findall(self.re_def, data)]
            if defenition:
                tr.add_type('', defenition)

            examples = [self.re_tags.sub('', w) for w in
                        re.findall(self.re_example, data)]
            if examples:
                tr.add_specification("examples", examples)

            refs = [self.re_tags.sub('', w) for w in
                    re.findall(self.re_refs, data)]
            if refs:
                tr.refs = refs

            return tr
        else:
            return None

    def get(self, regexp: str):
        return [w for w in self._words if re.match(regexp, w)]

    def load(self):
        print(f' {self.name} loading')
        self._words = [w.decode('utf-8') for w in self._dict.idx._idx]
        print(self._words)

    def resume(self):
        print(f' {self.name} resuming')
        pass

    def suspend(self):
        print(f' {self.name} suspend')
        self._dict.clear()  # clear cache

    def unload(self):
        print(f' {self.name} unloading')
        self._dict.clear()  # clear cache
        self._words.clear()

    def get_supported_langs(self) -> ():
        return self._langs

    def is_lang_supported(self, lang: str) -> bool:
        return lang in self._langs


if __name__ == '__main__':
    sd = Stardict(
        '/home/hd/mnt/dict/stardict-lingvo-ER-Biology-2.4.2/ER-Biology')
    # print(sd.translate('test'))
    sd.load()
    # print(sd._words)
    import re

    regex = '({}).*'
    w = input()
    print(regex.format(w))
    res = sd.get(regex.format(w))[0]
    print(res)
    print(sd.translate(res))

    # res = re.match(, 'test of smth')
    # if res:
    #    print(res)

from sptr.dictionary.base_dict import BaseDictionary


class CacheDictionaryProxy(BaseDictionary):
    def __init__(self, dictionary):
        self.dictionary = dictionary
        self.tr_cache = dict()
        self.get_cache = dict()

    def add_tr_to_cache(self, word: str, tr):
        self.tr_cache[word] = tr
        if len(self.tr_cache) + len(self.get_cache) > self.max_cache_size:
            self.tr_cache.popitem()
        return tr

    def translate(self, word: str):
        tr = self.tr_cache.get(str)
        if tr:
            return tr
        else:
            return self.add_tr_to_cache(
                word,
                self.dictionary.translate(word)
            )





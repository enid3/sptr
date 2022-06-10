from dataclasses import dataclass, field

from sptr.dictionary.base_dict import BaseDictionary


@dataclass
class Translated:
    origin: str
    clarification: str = ''
    definition: str = ''

    types: dict = field(default_factory=dict)
    specifications: dict = field(default_factory=dict)
    refs: list = field(default_factory=list)
    dictionary: BaseDictionary = None
    source: str = ''

    def add_type(self, type_name: str, descriptions: list):
        if type_name in self.types:
            self.types[type_name] += descriptions
        else:
            self.types[type_name] = descriptions

    def add_specification(self, spec_name: str, descriptions: list):
        if spec_name in self.specifications:
            self.specifications[spec_name] += descriptions
        else:
            self.specifications[spec_name] = descriptions

    def add_ref(self, ref: str):
        self.refs.append(ref)


class TestDict1(BaseDictionary):
    def __init__(self):
        super().__init__()
        self.name = 'Lingovo'

example = Translated('young', 'jʌŋ', '',
                     {'прил.':
                          ['молодой, юный', 'неопытный',
                           'недавний, новый',
                           '(the Younger) младший (о сыне в отличие от '
                           'отца, младшем брате в отличие от старшего)',
                           'разг. маленький, миниатюрный'],
                      'сущ.': ['(the young) употр. с гл. во мн. молодёжь',
                               '(youngs) вновь прибывшие, новички',
                               'употр. с гл. во мн. детёныши, потомство (животных)']
                      },
                     {
                         'Examples from texts': [
                             'From a distance, that mound of light-colored'
                             ' sand had seemed discolored with streaks of red,'
                             ' and as he moved closer, young Hralien realized '
                             'that the streaks weren’t discolored sand, '
                             'but were actually moving upon the surface of '
                             'the mound. '],
                     },
                     [],
                     dictionary=TestDict1(),
                     source='https://www.lingvolive.com/en-us/translate/en-ru/young')



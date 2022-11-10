import abc
from typing import List, Union, Tuple, Callable
from urllib.parse import quote_plus as urlquote
from Utility.strlib import is_chinese

Rect = Union[Tuple[int, int], Tuple[int, int, int, int]]

class Translator(metaclass=abc.ABCMeta):
    class Control:
        def __init__(self, rect: Rect, text: str, tooltip: str, keywork_url_callback: Callable[[str], str]):
            self.__rect: Rect = rect
            self.__text: str = text
            self.__tooltip: str = tooltip
            self.__keywork_url_callback: Callable[[str], str] = keywork_url_callback

        @property
        def rect(self):
            return self.__rect
        @property
        def text(self):
            return self.__text
        @property
        def tooltip(self):
            return self.__tooltip
        @property
        def keywork_url_callback(self):
            return self.__keywork_url_callback


    def __init__(self, n_rows: int, n_cols: int, default_translate_direction: str, ctrls: List[Union[Control, Tuple[Rect, str, str, Callable[[str], str]]]]):
        self.__n_rows: int = n_rows
        self.__n_cols: int = n_cols
        self.__default_translate_direction = default_translate_direction
        self.__ctrls: List[Translator.Control] = [c if isinstance(c, Translator.Control) else Translator.Control(*c) for c in ctrls]


    @property
    def n_rows(self):
        return self.__n_rows

    @property
    def n_cols(self):
        return self.__n_cols

    @property
    def default_translate_direction(self):
        return self.__default_translate_direction

    @property
    def ctrls(self):
        return [c for c in self.__ctrls]

    # @classmethod
    # def Translate(cls, keyword: str, direction: TranslateDirection) -> str:
    #     if direction == TranslateDirection.Auto:
    #         return cls._TranslateAuto(keyword)
    #     elif direction == TranslateDirection.CE:
    #         return cls._TranslateCE(keyword)
    #     elif direction == TranslateDirection.EC:
    #         return cls._TranslateEC(keyword)
    #     else:
    #         raise NotImplementedError(direction)
    # @classmethod
    # def _TranslateAuto(cls, keyword: str) -> str:
    #     return cls._TranslateCE(keyword) if any(is_chinese(c) for c in keyword) else cls._TranslateEC(keyword)
    # @classmethod
    # @abc.abstractmethod
    # def _TranslateCE(cls, keyword: str) -> str:
    #     return NotImplemented
    # @classmethod
    # @abc.abstractmethod
    # def _TranslateEC(cls, keyword: str) -> str:
    #     return NotImplemented

CE_info = ("CE", "CE (Chinese to English)")
EC_info = ("EC", "EC (English to Chinese)")
CE_or_EC_info = ("CE/EC", "CE if there are any Chinese characters: [\\u4e00-\\u9fff]\nEC otherwise")
CC_info = ("CC", "CC (Chinese to Chinese)")
EE_info = ("EE", "EE (English to English)")
CC_or_EE_info = ("CC/EE", "CC if there are any Chinese characters: [\\u4e00-\\u9fff]\nEE otherwise")
Term_to_Abbr_info = ("Term ➔ Abbr.", "Term ➔ Abbreviation")
Abbr_to_Term_info = ("Abbr. ➔ Term", "Abbreviation ➔ Term")

def SwichByChinese(chinese_callback: Callable[[str], str], english_callback: Callable[[str], str]):
    return lambda keyword: chinese_callback(keyword) if any(is_chinese(c) for c in keyword) else english_callback(keyword)

GoogleTranslate = Translator(2, 2, CE_or_EC_info[0], [
    ((0, 0), *CE_info, ce := lambda keyword: "https://translate.google.com.tw/#view=home&op=translate&sl=auto&tl=en&text=" + urlquote(keyword)),
    ((0, 1), *EC_info, ec := lambda keyword: "https://translate.google.com.tw/#view=home&op=translate&sl=auto&tl=zh-TW&text=" + urlquote(keyword)),
    ((1, 0, 1, 2), *CE_or_EC_info, SwichByChinese(ce, ec)),
])

YahooDictionary = Translator(2, 2, CE_or_EC_info[0], [
    ((0, 0), *CE_info, f := lambda keyword: "https://tw.dictionary.search.yahoo.com/search?p=" + urlquote(keyword)),
    ((0, 1), *EC_info, f),
    ((1, 0, 1, 2), *CE_or_EC_info, f),
])

Wikitionary = Translator(2, 7, CE_or_EC_info[0], [
    ((0, 0, 1, 2), *CE_info, to_e := lambda keyword: "https://en.wiktionary.org/wiki/" + urlquote(keyword)),
    ((0, 2, 1, 2), *EC_info, to_c := lambda keyword: "https://zh.wiktionary.org/wiki/" + urlquote(keyword)),
    ((0, 4, 1, 3), *CE_or_EC_info, SwichByChinese(to_e, to_c)),
    ((1, 0, 1, 2), *CC_info, to_c),
    ((1, 2, 1, 2), *EE_info, to_e),
    ((1, 4, 1, 3), *CC_or_EE_info, SwichByChinese(to_c, to_e)),
])

Abbreviation = Translator(2, 1, Abbr_to_Term_info[0], [
    ((0, 0), *Abbr_to_Term_info, lambda keyword: "https://www.abbreviations.com/" + urlquote(keyword)),
    ((1, 0), *Term_to_Abbr_info, lambda keyword: "https://www.abbreviations.com/abbreviation/" + urlquote(keyword)),
])
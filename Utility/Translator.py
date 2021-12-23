import abc
from urllib.parse import quote_plus as urlquote
from Utility.TranslateDirection import TranslateDirection
from Utility.strlib import is_chinese

class Translator(metaclass=abc.ABCMeta):
    @classmethod
    def Translate(cls, keyword: str, direction: TranslateDirection) -> str:
        if direction == TranslateDirection.Auto:
            return cls._TranslateAuto(keyword)
        elif direction == TranslateDirection.CE:
            return cls._TranslateCE(keyword)
        elif direction == TranslateDirection.EC:
            return cls._TranslateEC(keyword)
        else:
            raise NotImplementedError(direction)
    @classmethod
    def _TranslateAuto(cls, keyword: str) -> str:
        return cls._TranslateCE(keyword) if any(is_chinese(c) for c in keyword) else cls._TranslateEC(keyword)
    @classmethod
    @abc.abstractmethod
    def _TranslateCE(cls, keyword: str) -> str:
        return NotImplemented
    @classmethod
    @abc.abstractmethod
    def _TranslateEC(cls, keyword: str) -> str:
        return NotImplemented

class GoogleTranslate(Translator):
    @classmethod
    def _TranslateCE(cls, keyword: str) -> str:
        return 'https://translate.google.com.tw/#view=home&op=translate&sl=auto&tl=en&text=' + urlquote(keyword)
    @classmethod
    def _TranslateEC(cls, keyword: str) -> str:
        return 'https://translate.google.com.tw/#view=home&op=translate&sl=auto&tl=zh-TW&text=' + urlquote(keyword)

class BingTranslate(Translator):
    @classmethod
    def _TranslateCE(cls, keyword: str) -> str:
        return 'https://www.bing.com/Translator?to=en&from=zh-CHT&text=' + urlquote(keyword)
    @classmethod
    def _TranslateEC(cls, keyword: str) -> str:
        return 'https://www.bing.com/Translator?from=en&to=zh-CHT&text=' + urlquote(keyword)

class YahooDictionary(Translator):
    @classmethod
    def _TranslateCE(cls, keyword: str) -> str:
        return 'https://tw.dictionary.search.yahoo.com/search?p=' + urlquote(keyword)
    @classmethod
    def _TranslateEC(cls, keyword: str) -> str:
        return 'https://tw.dictionary.search.yahoo.com/search?p=' + urlquote(keyword)
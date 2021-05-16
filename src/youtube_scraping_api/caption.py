from bs4 import BeautifulSoup as bs
import requests

from typing import Optional, List, Dict, Union

class Caption():
    """Caption object of video"""
    def __init__(self, language_code: str, name: str, url, translatable: str = False, translate_langs: Optional[List] = None):
        self.language_code = language_code
        self.name = name
        self._url = url
        self.is_translatable = translatable
        self._trans_lang = translate_langs
    
    def __repr__(self):
        return f'<Caption lang="{self.name}" code="{self.language_code}" is_translatable={self.is_translatable}>'

    @property
    def available_translations(self) -> 'TransLangQuery':
        """Return all available translations of the caption
        
        :return: List of all available translations
        :rtype: List[TransLangQuery]
        """
        if self.is_translatable:
            return TransLangQuery(TranslationLang(i) for i in self._trans_lang)

    @property
    def xml(self) -> str:
        """Raw XML format of the caption

        :return: Caption in XML format
        :rtype: str
        """
        return requests.get(self._url).text

    def get_text(self, delimiter='\n') -> str:
        """Extract text from XML string

        :param delimiter: Delimiter for spliting sentences, defaults to '\\n'
        :type delimiter: str, optional
        :return: Caption in pure text form
        :rtype: str
        """
        raw = bs(self.xml, 'lxml')
        text = raw.findAll('text')
        string = [bs(i.text, 'lxml').text for i in text]
        return delimiter.join(string)

    @property
    def dict(self) -> Dict[str, Union[str, float]]:
        """GIves you a dictionary containing the captions content and metadata

        :return: Caption text and it's metadata in dictionary format
        :rtype: dict
        """
        raw = bs(self.xml, 'lxml')
        text = raw.findAll('text')
        return [{
            'start_from': float(i['start']),
            'duration': float(i['dur']),
            'text': bs(i.text, 'lxml').text
        } for i in text]

    def translate_to(self, language_code: str) -> Optional['TranslatedCaption']:
        """Translate the caption to the given language if the caption is translatable

        :param language_code: Language code of targeted language for translation
        :type language_code: str
        :return: Translated caption
        :rtype: TranslatedCaption
        """
        if self.is_translatable:
            if not language_code in self.available_translations.get_language_code():
                return None
            return TranslatedCaption(self.available_translations.get_language(language_code), self._url, self.language_code)

class TranslatedCaption(Caption):
    """Object of translated version of caption"""
    def __init__(self, language: 'TranslateLang', url: str, original_lang_code: str):
        super(TranslatedCaption, self).__init__(language.language_code, language.name , url)
        del Caption.translate_to

        self.language_code = language.language_code
        self.name = language.name
        self._url = url+'&tlang='+self.language_code
        self.original_language_code = original_lang_code
    
    def __repr__(self):
        return f'<TranslatedCaption lang="{self.name}" code="{self.language_code}" translated_from="{self.original_language_code}">'

class TranslationLang:
    """Translation language for translatable caption"""
    def __init__(self, raw: dict):
        self.name = raw["languageName"]["simpleText"]
        self.language_code = raw["languageCode"]

    def __repr__(self):
        return f'<TranslationLang name="{self.name}" code="{self.language_code}">'

class CaptionQuery(list):
    """Container of available captions of the video"""
    def __init__(self, data: list, default: int = 0):
        super(CaptionQuery, self).__init__(data)
        self.default=default

    def __repr__(self):
        return f'<CaptionQuery {list(self)}>'

    def get_caption(self, language_code: Optional[str] = None) -> Optional[Caption]:
        """Get caption by language code

        :param language_code: Language code of the caption, defaults set to None
        :type language_code: str, optional
        :return: Caption that corresponds to the language code. Return caption with default language if language_code is not specified. Return None if caption with the language code is not found.
        :rtype: Caption or None
        """
        if not language_code:
            return self[self.default]
        else:
            for i in self:
                if i.language_code == language_code:
                    return i

class TransLangQuery(list):
    """Container of language available for translation of a caption
    """
    def __init__(self, data: list):
        super(TransLangQuery, self).__init__(data)

    def get_language(self, language_code: str) -> Optional[TranslationLang]:
        """Get language by language code

        :param language_code: Language code of the language
        :type language_code: str
        :return: Language that corresponds to the language code. Return None if caption with the language code is not found.
        :rtype: List[TranslateLang] or None
        """
        for i in self:
            if i.language_code == language_code:
                return i

    def get_name(self) -> list:
        """Return name of all available languages
        
        :return: Name of all available languages
        :rtype: list
        """
        return [i.name for i in self]

    def get_language_code(self) -> list:
        """Return language code of all available languages

        :return: Language code of all available languages
        :rtype: list
        """
        return [i.language_code for i in self]
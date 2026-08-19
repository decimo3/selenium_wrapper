''' Module to retrieve message strings '''
# pylint: disable=too-few-public-methods
from importlib.resources import as_file, files
from dotenv import dotenv_values

class _I18n:
    ''' class to retrieve message strings '''
    data: dict
    def __init__(self, lang: str) -> None:
        resource = files('selenium_wrapper').joinpath('resources', f'{lang}.lang')
        if not resource.is_file():
            raise FileNotFoundError(
                "Language resource file not found! "
                "Check if language is available.")
        with as_file(resource) as lang_file:
            self.data = dotenv_values(lang_file)
    def __getattr__(self, name: str) -> str:
        value = self.data.get(name, '')
        if not value:
            raise KeyError(f'The language resource key {name} was not found!')
        return value

LANG = _I18n('pt-BR')

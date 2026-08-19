import pytest
from selenium_wrapper.multilang import _I18n


def test_must_pass_with_valid_culture():
    _I18n('pt-BR')

def test_must_fail_with_invalid_culture():
    with pytest.raises(FileNotFoundError):
        _I18n('abc')

def test_must_pass_with_valid_culture_valid_key():
    lang = _I18n('pt-BR')
    # cSpell: disable-next-line
    assert lang.EXECUTIONER_ARGS_MISS == 'Não foram passados argumentos para a função!'

def test_must_fail_with_valid_culture_invalid_key():
    lang = _I18n('pt-BR')
    with pytest.raises(KeyError):
        # pylint: disable-next=pointless-statement
        lang.INVALID_KEY

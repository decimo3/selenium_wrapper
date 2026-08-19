from subprocess import SubprocessError
import pytest
from selenium_wrapper.executioner import execute

def test_must_pass_with_existent_program():
    execute('date')

def test_must_fail_with_nonexistent_program():
    with pytest.raises(FileNotFoundError):
        execute('abc')

def test_must_fail_with_existent_program_and_invalid_arguments():
    with pytest.raises(SubprocessError):
        execute('date', '0')

import pytest
from selenium_wrapper.version import Version

def test_must_fail_with_no_provided_arg():
    with pytest.raises(ValueError):
        Version()

def test_must_pass_with_valid_str_arg():
    assert str(Version('1.2.3')) == '1.2.3.0'
    assert str(Version('1.2.3.4')) == '1.2.3.4'
    assert str(Version('1.2')) == '1.2.0.0'

def test_must_fail_with_invalid_str_arg():
    with pytest.raises(ValueError):
        Version('abc')
    with pytest.raises(ValueError):
        Version('1.2.3.4-rc')

def test_must_pass_with_valid_int_args():
    assert str(Version(1,2)) == '1.2.0.0'
    assert str(Version(1,2,3)) == '1.2.3.0'
    assert str(Version(1,2,3,4)) == '1.2.3.4'

def test_must_fail_with_invalid_int_args():
    with pytest.raises(ValueError):
        Version('1','2')
        Version(1,2,3,4,'a')

def test_must_pass_with_valid_comparisons():
    assert Version(0,0) == Version(0,0,0,0)
    assert Version(1,2) > Version(1,0)
    assert Version(1,0) < Version(1,2)
    assert Version(1,2) >= Version(1,0)
    assert Version(1,0) <= Version(1,2)
    assert Version(1,2) >= Version(1,2)
    assert Version(1,2) <= Version(1,2)
    assert Version(1,2,3,4) == Version('1.2.3.4')

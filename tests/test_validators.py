import pytest

from app.validators import (
    validate_user_input,
    validate_name,
    validate_email,
    validate_mobile,
    clean_mobile_number,
    clean_name)

def test_user_input_empty():
    with pytest.raises(ValueError, match="Fields can't be empty"):
        validate_user_input(" ", "alex@domain.com", "12345678911")

def test_user_input_valid():
    name, email, phone = validate_user_input(" Alex Rau ", "alex@domain.com", "0159-234-5678")
    assert name == "Alex Rau"
    assert email == "alex@domain.com"
    assert phone == "01592345678"

def test_valid_clean_name():
    assert clean_name("  Alex@ Rau-  1287  ") == "Alex Rau-"

def test_valid_clean_mobile():
    assert clean_mobile_number("  0159-234-5678") == "01592345678"

def test_valid_name_matches():
    assert validate_name("Alex Rau") == True
    assert validate_name("Anne-Marie") == True

def test_invalid_name_fails():
    assert validate_name("!!--") == False
    assert validate_name("  ") == False
    assert validate_name("A") == False

def test_valid_mobile_matches():
    assert validate_mobile("01592345678") == True

def test_invalid_mobile_fails():
    assert validate_mobile("12345") == False
    assert validate_mobile("12345abs!") == False

def test_valid_email_matches():
    assert validate_email("name@domain.com") == True

def test_invalid_email_fails():
    assert validate_email("name.com") == False
    assert validate_email("name@.com") == False
    assert validate_email("name@domain") == False
    assert validate_email("name@domain..com") == False


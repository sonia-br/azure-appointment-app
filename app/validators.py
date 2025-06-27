import re

def validate_user_input(name, email, mobile_number):

    if not name.strip() or not email.strip() or not mobile_number.strip():
        raise ValueError("Fields can't be empty")    
    
    name = clean_name(name)
    mobile_number = clean_mobile_number(mobile_number)
    email = email.strip()

    if not validate_name(name):
        raise ValueError("Invalid name. Name must contain at least 2 letters.")

    if not validate_email(email):
        raise ValueError("Invalid email.")
    
    if not validate_mobile(mobile_number):
        raise ValueError("Invalid mobile number. Number must contain only digits and 11 characters")
    

    return name, email, mobile_number


def clean_name(input):
    pattern = r"[^a-zA-Z\s\-]" #letters, spaces or hyphens
    name = re.sub(pattern, "", input).strip() #finds and removes by pattern
    return name #strip removes leading and trailing spaces

def clean_mobile_number(input):
    pattern = r"[^\d]" #digits only
    number = re.sub(pattern, "", input)
    return number


def validate_name(name):
    pattern = r"^[a-zA-Z\s\-]+$"

    if not re.fullmatch(pattern, name):
        return False
    
    letter_count = 0
    for char in name:
        if char.isalpha():
            letter_count += 1
    
    if letter_count < 2:
        return False
    
    return True

def validate_email(input):
    pattern = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$" #pattern name@domain.com
    email = re.fullmatch(pattern, input) #checks if fully matches pattern
    return bool(email)
    
def validate_mobile(number):
    if len(number) == 11:
        return number[0] == "0" and number[1] == "1" and number.isdigit()
    else:
        return False
    
 

# validate email uniqueness
# validate slot_id
# validate any international phone number
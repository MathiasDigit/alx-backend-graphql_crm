import re

def validate_phone_format(phone):
    pattern = re.compile(r"^\+?\d{10,15}$|^\d{3}-\d{3}-\d{4}$")
    return pattern.match(phone)

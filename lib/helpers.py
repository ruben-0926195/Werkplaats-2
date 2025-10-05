import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

def hash_password(password):
    return ph.hash(password)

def verify_password(stored_hash, provided_password):
    try:
        return ph.verify(stored_hash, provided_password)
    except VerifyMismatchError:
        return False

def check_password_strength(password):
    min_length = 8
    uppercase_regex = re.compile(r'[A-Z]')
    lowercase_regex = re.compile(r'[a-z]')
    digit_regex = re.compile(r'\d')
    special_char_regex = re.compile(r'[!@#$%^&*()_+{}[\]:;<>,.?~\\/-]')

    if len(password) < min_length:
        return False, "Weak: Password should be at least {} characters long".format(min_length)

    if not uppercase_regex.search(password) or not lowercase_regex.search(password):
        return False, "Weak: Password should contain at least one uppercase and one lowercase letter"

    if not digit_regex.search(password):
        return False, "Weak: Password should contain at least one digit"

    if not special_char_regex.search(password):
        return False, "Weak: Password should contain at least one special character"

    return True, "Strong: Password meets the criteria"
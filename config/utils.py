import re

from rest_framework.response import Response

from config.country_codes import get_country_dial_code


class UserUtils:
    """Utility class for User-related operations."""

    @staticmethod
    def format_full_name(user):
        """Return the authentication's full name."""
        return f"{user.first_name} {user.last_name}".strip()

    @staticmethod
    def normalize_country(country):
        """Normalize country to capitalize the first letter of each word"""
        return ' '.join(word.capitalize() for word in country.split())

    @staticmethod
    def capitalize_name(name):
        """Capitalize the first letter of each part of the name."""
        return ' '.join(part.capitalize() for part in name.split())

    @staticmethod
    def is_strong_password(password):
        """Check if the password is strong enough."""
        if (len(password) < 8 or
            not any(char.isdigit() for char in password) or
            not any(char.isupper() for char in password) or
            not any(char.islower() for char in password) or
            not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?/' for char in password)):
            return False
        return True

    @staticmethod
    def anonymize_email(email):
        """Anonymize the email address for privacy."""
        local, domain = email.split('@')
        if len(local) <= 2:
            local = local[0] + '*' * (len(local) - 1)
        else:
            local = local[0] + '*' * (len(local) - 2) + local[-1]
        return f"{local}@{domain}"

    @staticmethod
    def generate_password_hash(password):
        """Generate a hashed version of the password."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def verify_password_hash(password, hashed):
        """Verify if the password matches the hashed version."""
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest() == hashed

    @staticmethod
    def generate_username(first_name, last_name):
        """Generate a username based on first and last name."""
        base_username = (first_name[0] + last_name).lower()
        import random
        suffix = random.randint(100, 999)
        return f"{base_username}{suffix}"

    @staticmethod
    def generate_strong_password(length=12):
        """Generate a strong random password."""
        import random
        import string
        characters = string.ascii_letters + string.digits + '!@#$%^&*|?'
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    @staticmethod
    def normalize_phone_number(phone_number, country_code):
        """
        Normalize phone number based on country code.

        Args:
            phone_number: The phone number to normalize
            country_code: ISO 3166-1 alpha-2 country code (e.g., 'NG', 'US')

        Returns:
            Normalized phone number in E.164 format
        """
        if not phone_number:
            return ''

        # Remove all non-digit characters except +
        phone_number = re.sub(r'[^\d+]', '', phone_number)

        # Get country dial code
        dial_code = get_country_dial_code(country_code)
        if not dial_code:
            return phone_number  # Return original if country code not found

        # Remove the + from dial_code for comparison
        dial_code_digits = dial_code[1:]

        # Case 1: Starts with 0 (e.g., 08027872415)
        if phone_number.startswith('0'):
            phone_number = dial_code + phone_number[1:]

        # Case 2: Starts with country code and 0 (e.g., +23408027872415 or 23408027872415)
        elif phone_number.startswith(f'+{dial_code_digits}0'):
            phone_number = f'+{dial_code_digits}' + phone_number[len(dial_code_digits) + 2:]
        elif phone_number.startswith(f'{dial_code_digits}0'):
            phone_number = f'+{dial_code_digits}' + phone_number[len(dial_code_digits) + 1:]

        # Case 3: Starts with country code without + (e.g., 2348027872415)
        elif phone_number.startswith(dial_code_digits):
            phone_number = '+' + phone_number

        # Case 4: Already has + and country code (e.g., +2348027872415)
        elif phone_number.startswith(dial_code):
            pass  # Already in correct format

        # Case 5: Just the number without prefix (e.g., 8027872415)
        else:
            phone_number = dial_code + phone_number

        return phone_number


class ResponseUtils:
    """Utility class for standardized API responses."""

    @staticmethod
    def success_response(message, data=None, status_code=200):
        """Return a standardized success response."""
        response_data = {
            'status_code': status_code,
            'status': 'success',
            'message': message,
        }
        if data is not None:
            response_data['data'] = data
        return Response(response_data, status=status_code)

    @staticmethod
    def error_response(message, errors=None, status_code=400):
        """Return a standardized error response."""
        response_data = {
            'status_code': status_code,
            'status': 'error',
            'message': message,
        }
        if errors is not None:
            response_data['errors'] = errors
        return Response(response_data, status=status_code)

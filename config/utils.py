class UserUtils:
    """Utility class for User-related operations."""

    @staticmethod
    def format_full_name(user):
        """Return the authentication's full name."""
        return f"{user.first_name} {user.last_name}".strip()

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
        characters = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?/'
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

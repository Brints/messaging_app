from django.contrib.auth import authenticate
from rest_framework import serializers

from apps.authentication.models import User
from config.utils import UserUtils


def validate_email(value):
    """Validate that the email is unique."""
    if not value:
        raise serializers.ValidationError("Email field cannot be empty.")
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError("A authentication with this email already exists.")
    return value


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    full_name = serializers.SerializerMethodField()
    display_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'full_name',
            'display_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def get_full_name(self, obj):
        """Return the authentication's full name."""
        return f"{obj.first_name} {obj.last_name}".strip()

class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for creating a new User."""
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'password',
            'confirm_password',
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_password(self, value):
        """Validate password strength."""
        if not UserUtils.is_strong_password(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters long and include "
                "uppercase, lowercase, digit, and special character."
            )

    def validate(self, data):
        """Validate that password and confirm_password match."""
        if data['password'] != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        data.pop('confirm_password')

        data['first_name'] = UserUtils.capitalize_name(data['first_name'])
        data['last_name'] = UserUtils.capitalize_name(data['last_name'])

        if not data.get('username'):
            data['username'] = UserUtils.generate_username(data['first_name'], data['last_name'])

        return data

    def create(self, validated_data):
        """Create and return a new User instance."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for authentication login."""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        """Validate email and password."""
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context['request'], username=email, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid email or password.")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        data['authentication'] = user
        return data

class PasswordGenerateSerializer(serializers.Serializer):
    """Serializer for generating a strong password."""
    length = serializers.IntegerField(min_value=8, max_value=128, default=12)

    def validate_length(self, value):
        """Validate password length."""
        if value < 8:
            raise serializers.ValidationError("Password length must be at least 8 characters.")
        return value

    def create(self, validated_data):
        """Generate and return a strong password."""
        length = validated_data.get('length', 12)
        password = UserUtils.generate_strong_password(length)
        return {'password': password}
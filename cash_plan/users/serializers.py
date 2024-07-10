from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from users.models import User, Currency

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email format.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in '!@#$%^&*()_+-=[]{}|;:\'",.<>?/' for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, data):
        # Validate password first
        self.validate_password(data.get('password'))
        
        # If password is valid, validate email
        self.validate_email(data.get('email'))
        
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        
        # Manually check if the email is already in use
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        
        user_obj = User.objects.create(
            email=email,
            password=make_password(password)
        )
        return user_obj

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username_or_email = attrs.get('email')
        password = attrs.get('password')

        # Attempt to authenticate the user first by email
        user = authenticate(username=username_or_email, password=password)

        if user:
            attrs['user'] = user
            return attrs
        else:
            raise AuthenticationFailed('Invalid credentials.')

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['name', 'full_name']

class UserSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = User
        fields = ['currency', 'balance', 'daily_amount']

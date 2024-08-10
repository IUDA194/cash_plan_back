from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from users.models import User
from currency.serializers import CurrencySerializer

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

class UserSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = User
        fields = ['currency', 'balance', 'daily_amount']

class UserUpdateCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['currency']

class UserUpdateDailyAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['daily_amount']

    def validate_daily_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Daily amount must be a positive number.")

        return value

    def update(self, instance, validated_data):
        old_daily_amount = instance.daily_amount or 0

        new_daily_amount = validated_data.get('daily_amount', old_daily_amount)

        difference = new_daily_amount - old_daily_amount

        instance.balance += difference

        instance.daily_amount = new_daily_amount

        instance.save()

        return instance
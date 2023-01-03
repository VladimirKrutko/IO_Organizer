from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
# from page_se.serializers import PageSerializer
import uuid


class UserRegistration(serializers.ModelSerializer):
    """
    Class for registration new users in system
    """
    email = serializers.CharField(max_length=200)
    username = serializers.CharField(max_length=200)
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token')

    def validate(self, data):
        """
        Validate data before create user
        """
        if not data['email']:
            raise serializers.ValidationError('Please input email')

        if not data['password']:
            raise serializers.ValidationError('Please input password')

        return data

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        for key, value in validated_data:
            setattr(instance, key, value)

        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email')

    def update(self, instance, validated_data):
        for key, value in validated_data:
            setattr(instance, key, value)

        instance.save()
        return instance

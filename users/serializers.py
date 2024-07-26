from rest_framework import serializers
from social_network.common.enum import ErrorMessages
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"], password=validated_data["password"]
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, min_length=8, max_length=128, write_only=True
    )

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password")

        try:
            user = User.objects.get(email__iexact=email)
            if not user.check_password(password):
                raise serializers.ValidationError(ErrorMessages.INVALID_PASSWORD.value)
        except User.DoesNotExist:
            raise serializers.ValidationError(ErrorMessages.USER_NOT_FOUND.value)

        return data

from friends.models import FriendRequest
from rest_framework import serializers
from social_network.common.enum import ErrorMessages
from users.models import User
from users.serializers import UserSerializer
from django.db.models import Q


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ["id", "sender", "status", "created_at", "updated_at"]


class SendFriendRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    def validate(self, data):
        email = data.get("email", "")

        try:
            receiver = User.objects.get(email__iexact=email)
            sender = self.context["request"].user

            if FriendRequest.objects.filter(
                Q(sender=sender, receiver=receiver, status="pending")
                | Q(sender=receiver, receiver=sender, status="pending")
            ).exists():
                raise serializers.ValidationError(
                    ErrorMessages.FRIEND_REQUEST_EXISTS.value
                )
            elif FriendRequest.objects.filter(
                Q(sender=sender, receiver=receiver, status="accepted")
                | Q(sender=receiver, receiver=sender, status="accepted")
            ).exists():
                raise serializers.ValidationError(
                    ErrorMessages.ALREADY_FRIENDS.value.format(receiver)
                )

        except User.DoesNotExist:
            raise serializers.ValidationError(ErrorMessages.USER_NOT_FOUND.value)

        return data


class FriendRequestActionSerializer(serializers.Serializer):
    action = serializers.ChoiceField(required=True, choices=["accept", "reject"])

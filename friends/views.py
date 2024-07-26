from social_network.common.enum import ErrorMessages, SuccessMessages
from social_network.common.resources import PrivateResource
from rest_framework import status
from users.models import User
from friends.models import Friend, FriendRequest
from friends.serializers import (
    FriendRequestActionSerializer,
    FriendRequestSerializer,
    SendFriendRequestSerializer,
)
from users.serializers import UserSerializer
from social_network.common.utils import ResponseUtils, SendFriendRequestThrottle


class FriendsListView(PrivateResource):
    def get(self, request):
        user = request.user
        friends = Friend.objects.get(owner=user).friends.all()
        serializer = UserSerializer(friends, many=True)

        return ResponseUtils.format_success_response(
            response=serializer.data, code=status.HTTP_200_OK
        )


class PendingFriendRequestsView(PrivateResource):
    def get(self, request):
        user = request.user
        pending_requests = FriendRequest.objects.filter(receiver=user, status="pending")
        serializer = FriendRequestSerializer(pending_requests, many=True)

        return ResponseUtils.format_success_response(
            response=serializer.data, code=status.HTTP_200_OK
        )


class SendFriendRequest(PrivateResource):
    throttle_classes = [SendFriendRequestThrottle]

    def post(self, request):
        serializer = SendFriendRequestSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            to_user_email = request.data.get("email")
            receiver = User.objects.get(email__iexact=to_user_email)
            sender = request.user

            friend_request = FriendRequest(
                sender=sender, receiver=receiver, status="pending"
            )
            friend_request.save()

            return ResponseUtils.format_success_response(
                response={},
                message=SuccessMessages.REQUEST_SUCCESS.value,
                code=status.HTTP_201_CREATED,
            )
        else:
            return ResponseUtils.format_error_response(
                response=serializer.errors, code=status.HTTP_400_BAD_REQUEST
            )


class FriendRequestResponseView(PrivateResource):
    def put(self, request, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(
                id=friend_request_id, receiver=request.user
            )

            if not friend_request.status == "pending":
                fr_status = (
                    "accepted" if friend_request.status == "accepted" else "rejected"
                )

                return ResponseUtils.format_error_response(
                    response={
                        "error": ErrorMessages.FRIEND_REQUEST_ACTION_ALREADY_UPDATED.value.format(
                            fr_status
                        )
                    },
                    code=status.HTTP_400_BAD_REQUEST,
                )

            serializer = FriendRequestActionSerializer(data=request.data)

            if serializer.is_valid():
                action = request.data.get("action")

                if action == "accept":
                    friend_request.status = "accepted"
                    Friend.add_friend(request.user, friend_request.sender)
                    Friend.add_friend(friend_request.sender, request.user)
                    message = SuccessMessages.REQUEST_ACCEPTED_SUCCESS.value
                elif action == "reject":
                    friend_request.status = "rejected"
                    message = SuccessMessages.REQUEST_REJECTED_SUCCESS.value
                friend_request.save()

                return ResponseUtils.format_success_response(
                    response={},
                    message=message,
                    code=status.HTTP_200_OK,
                )
            else:
                return ResponseUtils.format_error_response(
                    response=serializer.errors, code=status.HTTP_400_BAD_REQUEST
                )
        except FriendRequest.DoesNotExist:
            return ResponseUtils.format_error_response(
                response=ErrorMessages.FRIEND_REQUEST_DOES_NOT_EXISTS.value,
                code=status.HTTP_404_NOT_FOUND,
            )

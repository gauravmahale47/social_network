from friends.views import (
    FriendsListView,
    PendingFriendRequestsView,
    SendFriendRequest,
    FriendRequestResponseView,
)
from django.urls import path

app_name = "friends"

urlpatterns = [
    path("", FriendsListView.as_view(), name="friends-list"),
    path("send-request/", SendFriendRequest.as_view(), name="friend-request"),
    path(
        "request-action/<int:friend_request_id>/",
        FriendRequestResponseView.as_view(),
        name="friend-request-response",
    ),
    path(
        "pending-requests/",
        PendingFriendRequestsView.as_view(),
        name="pending-requests",
    ),
]

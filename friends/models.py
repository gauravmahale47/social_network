from django.db import models
from social_network.common.models import BaseModel
from users.models import User


class FriendRequest(BaseModel):
    sender = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
    )

    class Meta:
        db_table = "friend_requests"

    def __str__(self):
        return self.sender.email


class Friend(BaseModel):
    friends = models.ManyToManyField(User, related_name="friends")
    owner = models.OneToOneField(User, related_name="owners", on_delete=models.CASCADE)

    class Meta:
        db_table = "friends"

    def __str__(self):
        return self.owner.email

    @classmethod
    def add_friend(cls, owner, new_friend):
        instance, created = cls.objects.get_or_create(owner=owner)
        instance.friends.add(new_friend)

    @classmethod
    def remove_friend(cls, owner, new_friend):
        instance, created = cls.objects.get_or_create(owner=owner)
        instance.friends.remove(new_friend)

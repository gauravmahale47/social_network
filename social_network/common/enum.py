from enum import Enum


class SuccessMessages(Enum):
    SIGNUP_SUCCESS = "You have signed up successfully."
    LOGIN_SUCCESS = "You have logged in successfully."
    REQUEST_SUCCESS = "Friend request sent successfully."
    REQUEST_ACCEPTED_SUCCESS = "Friend request accepted successfully."
    REQUEST_REJECTED_SUCCESS = "Friend request rejected successfully."


class ErrorMessages(Enum):
    USER_NOT_FOUND = "User not found."
    INVALID_EMAIL = "Invalid email address."
    INVALID_PASSWORD = "Invalid password."
    INVALID_SEARCH_PARAMS = "Invalid search params."
    FRIEND_REQUEST_EXISTS = "Friend request already sent."
    ALREADY_FRIENDS = "You and {0} are already friends."
    FRIEND_REQUEST_DOES_NOT_EXISTS = "Friend request does not exists."
    FRIEND_REQUEST_ACTION_ALREADY_UPDATED = "Friend request already {0}."

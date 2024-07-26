from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import UserRateThrottle


class CoreUtils(object):
    pass


class ResponseUtils(object):
    @staticmethod
    def format_success_response(response, code, message=None):
        if message is not None:
            return Response(
                {
                    "data": response,
                    "message": message,
                },
                status=code,
            )
        else:
            return Response(
                {"data": response},
                status=code,
            )

    @staticmethod
    def format_error_response(response, code):
        return Response({"errors": response}, status=code)


class Pagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 10


class SendFriendRequestThrottle(UserRateThrottle):
    scope = "send_friend_request"
    rate = "3/minute"

    def get_cache_key(self, request, view):
        if not request.user.is_authenticated:
            return None  # Only authenticated users are throttled

        return self.cache_format % {
            "scope": self.scope,
            "ident": request.user.pk,  # Use user ID for rate limiting
        }

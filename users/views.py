from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from social_network.common.enum import SuccessMessages, ErrorMessages
from social_network.common.resources import PublicResource, PrivateResource
from social_network.common.utils import ResponseUtils
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, UserLoginSerializer
from django.db.models import Q
from social_network.common.utils import Pagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class SignUpView(PublicResource):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return ResponseUtils.format_success_response(
                response=serializer.data,
                message=SuccessMessages.SIGNUP_SUCCESS.value,
                code=status.HTTP_201_CREATED,
            )
        else:
            return ResponseUtils.format_error_response(
                response=serializer.errors, code=status.HTTP_400_BAD_REQUEST
            )


class LogInView(PublicResource):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = request.data.get("email")
            user = User.objects.get(email__iexact=email)
            refresh = RefreshToken.for_user(user)

            return ResponseUtils.format_success_response(
                response={"refresh": str(refresh), "access": str(refresh.access_token)},
                message=SuccessMessages.LOGIN_SUCCESS.value,
                code=status.HTTP_200_OK,
            )
        else:
            return ResponseUtils.format_error_response(
                response=serializer.errors, code=status.HTTP_400_BAD_REQUEST
            )


class UserSearchView(PrivateResource):
    @method_decorator(cache_page(60 * 1))  # Cache for 1 minute
    def get(self, request):
        query = request.query_params.get("q", "")
        if query:
            users = users = User.objects.filter(
                Q(email__iexact=query) | Q(name__icontains=query)
            )
            paginator = Pagination()
            paginated_users = paginator.paginate_queryset(users, request)
            serializer = UserSerializer(paginated_users, many=True)

            return paginator.get_paginated_response(serializer.data)
        else:
            return Response(
                {"error": ErrorMessages.INVALID_SEARCH_PARAMS.value},
                status=status.HTTP_400_BAD_REQUEST,
            )

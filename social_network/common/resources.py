from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny


class PrivateResource(APIView):
    permission_classes = [IsAuthenticated]


class PublicResource(APIView):
    permission_classes = [AllowAny]

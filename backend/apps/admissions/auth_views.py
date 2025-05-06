from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response(
            {"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response(
        {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def get_user(request):
    if not request.user.is_authenticated:
        return Response(
            {"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED
        )

    return Response(
        {
            "id": request.user.id,
            "username": request.user.username,
            "email": request.user.email,
            "is_staff": request.user.is_staff,
        }
    )

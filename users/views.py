from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from recipe.models import Recipe
from .models import Profile
from recipe.serializers import RecipeSerializer
from . import serializers
User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    """
    API view to register a new User.
    """
    serializer = serializers.UserRegisterationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = RefreshToken.for_user(user)
    data = serializer.data
    data['tokens'] = {
        'refresh': str(token),
        'access': str(token.access_token)
    }
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    API view to authenticate existing users using their email and password.
    """
    serializer = serializers.UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    serializer = serializers.CustomUserSerializer(user)
    token = RefreshToken.for_user(user)
    data = serializer.data
    data['tokens'] = {
        'refresh': str(token),
        'access': str(token.access_token)
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    API view to logout users.
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    API view to get and update user information.
    """
    user = request.user
    if request.method == 'GET':
        serializer = serializers.CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.CustomUserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile_update(request):
    """
    API view to get and update user profile.
    """
    profile = request.user.profile
    if request.method == 'GET':
        serializer = serializers.ProfileSerializer(profile)
        print(serializer.data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_avatar(request):
    """
    API view to get and update user avatar.
    """
    profile = request.user.profile
    if request.method == 'GET':
        serializer = serializers.ProfileAvatarSerializer(profile)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = serializers.ProfileAvatarSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_bookmarks(request, pk):
    """
    Get, Create, Delete favorite recipe
    """
    profile = Profile.objects.all()

    if request.method == 'GET':
        user = User.objects.get(id=pk)

        user_profile = get_object_or_404(profile, user=user)
        print(user_profile)
        serializer = RecipeSerializer(user_profile.bookmarks.all(), many=True)
        print(serializer)
        print(user_profile.bookmarks)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = User.objects.get(id=pk)
        print(user)
        user_profile = get_object_or_404(profile, user=user)
        print(user_profile)
        recipe = Recipe.objects.get(id=request.data['id'])
        print(recipe)
        if user_profile:
            user_profile.bookmarks.add(recipe)
            user_profile.save()
            recipe.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user = User.objects.get(id=pk)
        user_profile = get_object_or_404(profile, user=user)
        recipe = Recipe.objects.get(id=request.data['id'])
        if user_profile:
            user_profile.bookmarks.remove(recipe)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    """
    API view to get, create, and delete favorite recipes.
    """
  


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def password_change(request):
    """
    API view for changing user password.
    """
    serializer = serializers.PasswordChangeSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

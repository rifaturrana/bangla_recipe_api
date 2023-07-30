from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Recipe, RecipeLike, RecipeBookmark
from .serializers import RecipeLikeSerializer, RecipeSerializer
from .permissions import IsAuthorOrReadOnly


@api_view(['GET'])
@permission_classes([AllowAny])
def recipe_list(request):
    """
    Get a collection of recipes.
    """
    queryset = Recipe.objects.all()
    serializer = RecipeSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    """
    Create a recipe.
    """
    serializer = RecipeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(author=request.user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthorOrReadOnly])
def recipe_detail(request, pk):
    """
    Get, update, or delete a recipe.
    """
    recipe = get_object_or_404(Recipe, id=pk)

    if request.method == 'GET':
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = RecipeSerializer(recipe, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def recipe_like(request, pk):
    """
    Like or dislike a recipe.
    """
    recipe = get_object_or_404(Recipe, id=pk)

    if request.method == 'POST':
        new_like, created = RecipeLike.objects.get_or_create(user=request.user, recipe=recipe)
        if created:
            new_like.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
            if like.exists():
                like.delete()
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def recipe_bookmark(request, pk):
    """
    Bookmark or unbookmark a recipe.
    """
    recipe = get_object_or_404(Recipe, id=pk)

    if request.method == 'POST':
        new_bookmark, created = RecipeBookmark.objects.get_or_create(user=request.user, recipe=recipe)
        if created:
            new_bookmark.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            bookmark = RecipeBookmark.objects.filter(user=request.user, recipe=recipe)
            if bookmark.exists():
                bookmark.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        bookmark = RecipeBookmark.objects.filter(user=request.user, recipe=recipe)
        if bookmark.exists():
            bookmark.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    
   

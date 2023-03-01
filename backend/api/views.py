from datetime import datetime as dt
from urllib.parse import unquote

from django.http.response import HttpResponse
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import User

from .filters import RecipeFilter
from .mixins import AddDelViewMixin
from .paginators import PageLimitPagination
from .permissions import (AdminOrReadOnly, AuthenticatedAndNotAnonymous,
                          AuthorStaffOrReadOnly)
from .serializers import (FollowSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer)


class UserViewSet(DjoserUserViewSet, AddDelViewMixin):
    pagination_class = PageLimitPagination
    add_serializer = FollowSerializer
    permission_classes = [AuthenticatedAndNotAnonymous]

    @action(
        methods=(
            "GET",
            "POST",
            "DELETE",
        ),
        detail=True,
    )
    def subscribe(self, request, id):
        return self.add_remove_relation(id, "follow_M2M")

    @action(methods=("get",), detail=False)
    def subscriptions(self, request):
        user = self.request.user
        authors = user.follow.all()
        pages = self.paginate_queryset(authors)
        serializer = FollowSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset
        if name:
            if name[0] == "%":
                name = unquote(name)
            name = name.lower()
            stw_queryset = list(queryset.filter(name__startswith=name))
            cnt_queryset = queryset.filter(name__contains=name)
            stw_queryset.extend(
                [i for i in cnt_queryset if i not in stw_queryset]
            )
            queryset = stw_queryset
        return queryset


class RecipeViewSet(ModelViewSet, AddDelViewMixin):
    queryset = Recipe.objects.select_related("author")
    serializer_class = RecipeSerializer
    permission_classes = (AuthorStaffOrReadOnly,)
    pagination_class = PageLimitPagination
    add_serializer = ShortRecipeSerializer
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = self.queryset

        tags = self.request.query_params.getlist("tags")
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()

        author = self.request.query_params.get("author")
        if author:
            queryset = queryset.filter(author=author)

        user = self.request.user
        if user.is_anonymous:
            return queryset
        
        q_filter = RecipeFilter(self.request.query_params)
        queryset = q_filter.filter_queryset(queryset, user)

        return queryset

    @action(
        methods=(
            "GET",
            "POST",
            "DELETE",
        ),
        detail=True,
    )
    def favorite(self, request, pk):
        return self.add_remove_relation(pk, "is_favorite_M2M")

    @action(
        methods=(
            "GET",
            "POST",
            "DELETE",
        ),
        detail=True,
    )
    def shopping_cart(self, request, pk):
        return self.add_remove_relation(pk, "shopping_cart_M2M")

    @action(methods=("get",), detail=False)
    def download_shopping_cart(self, request):
        user = self.request.user
        recipe = Recipe.objects.filter(is_in_shopping_list=user).first()
        if not recipe:
            return Response(status=HTTP_400_BAD_REQUEST)
        return recipe.download_shopping_cart(user)

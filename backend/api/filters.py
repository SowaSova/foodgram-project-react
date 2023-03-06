from django_filters import rest_framework as filters

from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    is_in_shopping_cart = filters.BooleanFilter(
        field_name="is_in_shopping_list", method="filter_is_in_shopping_cart"
    )
    is_favorited = filters.BooleanFilter(
        field_name="is_favorite", method="filter_is_favorited"
    )

    class Meta:
        model = Recipe
        fields = ("author", "tags")

    def __init__(self, *args, **kwargs):
        self.request = kwargs["request"]
        super().__init__(*args, **kwargs)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(is_in_shopping_list=user)
        return queryset.exclude(is_in_shopping_list=user)

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(is_favorite=user)
        return queryset.exclude(is_favorite=user)

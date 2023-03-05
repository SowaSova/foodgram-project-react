from django.contrib.admin import ModelAdmin, TabularInline, register

from .models import Ingredient, IngredientInRecipe, Recipe, Tag

EMPTY_VALUE_DISPLAY = "--None--"


class IngredientInLine(TabularInline):
    model = IngredientInRecipe
    extra = 2


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ("name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ("name", "color", "slug")
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        "name",
        "author",
    )
    list_filter = (
        "name",
        "author",
        "tags",
    )
    search_fields = (
        "name",
        "author",
        "tags",
    )
    empty_value_display = EMPTY_VALUE_DISPLAY
    inlines = (IngredientInLine,)
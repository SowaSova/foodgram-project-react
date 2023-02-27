from django.contrib.admin import register, ModelAdmin, TabularInline

from .models import (
    Ingredient,
    Tag,
    Recipe,
    IngredientInRecipe,
)

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
        "add_in_favorites",
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
    readonly_fields = ("add_in_favorites",)
    inlines = (IngredientInLine, )

    def add_in_favorites(self, obj):
        return obj.favorites_list.count()

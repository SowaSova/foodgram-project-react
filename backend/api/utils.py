from rest_framework.serializers import ValidationError

from recipes.models import IngredientInRecipe


def enter_ingredient_quantity_in_recipe(recipe, ingredients):
    for ingredient in ingredients:
        IngredientInRecipe.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient["ingredient"],
            amount=ingredient["amount"],
        )


def check_value_validate(value, klass=None):
    if not str(value).isdecimal():
        raise ValidationError(f"{value} должно содержать цифру")
    if klass:
        obj = klass.objects.filter(id=value)
        if not obj:
            raise ValidationError(f"{value} не существует")
        return obj[0]

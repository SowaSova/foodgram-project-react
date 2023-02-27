from recipes.models import IngredientInRecipe


def enter_ingredient_quantity_in_recipe(recipe, ingredients):
    for ingredient in ingredients:
        IngredientInRecipe.objects.get_or_create(
            recipe=recipe,
            ingredients=ingredient['ingredient'],
            amount=ingredient['amount']
        )
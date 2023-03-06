from colorfield.fields import ColorField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import F, Sum, UniqueConstraint
from django.http import HttpResponse
from django.utils import timezone as tz

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        "Название тега",
        max_length=200,
        unique=True,
        db_index=True,
    )
    color = ColorField(
        verbose_name="Цвет в HEX",
        default="#FF0000",
    )
    slug = models.SlugField(
        "Уникальный слаг",
        unique=True,
        max_length=200,
        db_index=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return f"{self.name} {self.color}"


class Ingredient(models.Model):
    name = models.CharField(
        "Название ингредиента",
        max_length=200,
        db_index=True,
    )
    measurement_unit = models.CharField("Ед. измерения", max_length=10)

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name}, {self.measurement_unit}"


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        db_index=True,
    )
    name = models.CharField(
        "Название рецепта",
        max_length=200,
        db_index=True,
    )
    text = models.TextField(
        "Описание",
        max_length=2000,
    )
    image = models.ImageField(
        "Картинка", upload_to="media/recipes/images/", blank=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовление (мин.)",
        default=1,
        validators=[MinValueValidator(1, message="Меньше минуты?")],
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name="ingredients",
        through="IngredientInRecipe",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        db_index=True,
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_favorite = models.ManyToManyField(
        User, verbose_name="Избранное", related_name="favorites"
    )
    is_in_shopping_list = models.ManyToManyField(
        User, verbose_name="Список покупок", related_name="shopping_list"
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def get_shopping_list(self, user):
        if not user.is_authenticated:
            return None
        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe=self,
                recipe__is_in_shopping_list=True,
                recipe__author=user,
            )
            .values(
                ingredient_name=F("ingredient__name"),
                measure=F("ingredient__measurement_unit"),
            )
            .annotate(amount=Sum("amount"))
        )

        return ingredients

    def create_shopping_list(self, user, filename=None):
        TIME_FORMAT = "%d/%m/%Y %H:%M"
        ingredients = self.get_shopping_list(user)

        if not ingredients:
            return None

        shopping_list = (
            f"Список покупок для пользователя {user.first_name}:\n\n"
        )
        for ing in ingredients:
            shopping_list += (
                f'{ing["ingredient"]}: {ing["amount"]} {ing["measure"]}\n'
            )

        shopping_list += (
            f"\nДата составления {tz.now().strftime(TIME_FORMAT)}."
        )

        if filename:
            with open(filename, "w") as f:
                f.write(shopping_list)

        return shopping_list

    def __str__(self):
        return f"{self.name}"


class IngredientInRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name="ingredient_in_recipe",
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredient_in_recipe"
    )
    amount = models.PositiveSmallIntegerField(
        "Количество",
        validators=[MinValueValidator(1, message="Не меньше одного!")],
    )

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        constraints = [
            UniqueConstraint(
                fields=["ingredient", "recipe"],
                name="unique_ingredient_recipe",
            )
        ]

    def __str__(self):
        return f"{self.ingredient}, {self.recipe}, {self.amount}"

from django.db import models
from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import UniqueConstraint

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        "Название тега",
        max_length=200,
        unique=True,
    )
    color = ColorField(
        verbose_name="Цвет в HEX",
        default="#FF0000",
    )
    slug = models.SlugField(
        "Уникальный слаг",
        unique=True,
        max_length=200,
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
    )
    name = models.CharField("Название рецепта", max_length=200)
    text = models.TextField(
        "Описание",
        max_length=2000,
    )
    image = models.ImageField(
        "Картинка", upload_to="recipes/images/", blank=True
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

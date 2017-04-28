from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    notes = models.TextField()
    category = models.ForeignKey(Category, related_name='ingredients')
    other_ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name


class Chef(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField('Ingredient', related_name='chef', through='ChefIngredients')

    def __str__(self):
        return self.name


class ChefIngredients(models.Model):
    chef = models.ForeignKey(Chef)
    ingredient = models.ForeignKey(Ingredient)
from django.contrib import admin

# Register your models here.
from .models import Ingredient, Category, Chef, ChefIngredients

admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Chef)
admin.site.register(ChefIngredients)
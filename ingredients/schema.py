from graphene import relay, ObjectType, AbstractType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
import graphene
from ingredients.models import Category, Ingredient, Chef


class ChefType(DjangoObjectType):

    class Meta:
        model = Chef

# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        filter_fields = ['name', 'ingredients']



class IntroduceCategory(graphene.Mutation):

    class Input:
        category_name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, input, context, info):
        category_name = input.get('category_name')
        category = Category.objects.create(name=category_name)
        category.save()
        return IntroduceCategory(category=category)

class UpdateCategory(graphene.Mutation):

    class Input:
        category_name = graphene.String(required=True)
        category_id = graphene.Int(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, input, context, info):
        category_name = input.get('category_name')
        category = Category.objects.get(id=input.get("category_id"))
        category.name = category_name
        category.save()
        return IntroduceCategory(category=category)

class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'notes': ['exact', 'icontains'],
            'category': ['exact'],
            'category__name': ['exact'],
        }

class CreateIngredient(graphene.Mutation):

    class Input:
        ingredient_name = graphene.String(required=True)
        ingredient_notes = graphene.String(required=True)
        category_id = graphene.Int(required=True)

    ingredient = graphene.Field(IngredientType)
    @classmethod
    def mutate(cls, input, context, info):
        ingredient = Ingredient.objects.create(
            name = input.get('ingredient_name'),
            notes = input.get('ingredient_notes'),
            category_id = input.get('category_id')
        )
        ingredient.save()
        return CreateIngredient(ingredient=ingredient)



class Query(AbstractType):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)
    all_chefs = graphene.List(ChefType)
    hello = graphene.String(name=graphene.Argument(graphene.String, default_value="world"))


    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())

    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())

    def resolve_all_chefs(self, args, context, info):
        return Chef.objects.all()

    def resolve_all_categories(self, args, context, info):
        return Category.objects.all()

    def resolve_all_ingredients(self, args, context, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.all()


    def resolve_hello(self, args, context, info):
        return 'Hello ' + args['name']

    def resolve_category(self, args, context, info):
        id = args.get('id')
        name = args.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.filter(name=name).first()

        return None

    def resolve_ingredient(self, args, context, info):
        id = args.get('id')
        name = args.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.filter(name=name)

        return None


class Mutation(graphene.ObjectType):
    introduce_category = IntroduceCategory.Field()
    update_category = UpdateCategory.Field()
    create_ingredient = CreateIngredient.Field()
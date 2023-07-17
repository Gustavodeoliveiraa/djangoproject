from .test_recipe_base import RecipeTestBase, Recipe
from django.core.exceptions import ValidationError
from parameterized import parameterized


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_no_default(self):
        recipe = Recipe(
            category=self.make_category(name='test default category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug-no-default',
            preparation_time=10,
            preparation_time_unit='minutos',
            serving=5,
            serving_unit='Porções',
            preparation_step=False,
        )
        recipe.full_clean()
        recipe.save()
        return recipe

# parametrização teste
    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('serving_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_default()

        # vai falhar se se o valor default for mudado nos models
        self.assertFalse(recipe.preparation_step_is_html)

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_default()

        # vai falhar se se o valor default for mudado nos models
        self.assertFalse(recipe.is_published)

    def test_recipe_string_representation(self):
        need = 'Testing Representation'
        self.recipe.title = "Testing Representation"
        self.recipe.full_clean()
        self.recipe.save()

        self.assertEqual(
            str(self.recipe), need,
            msg=f'Recipe string representation must be "{need}" \
            but "{str(self.recipe.title)}" was received'
        )

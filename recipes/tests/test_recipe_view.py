from django.test import TestCase
from recipes.views import home, category, recipe
from django.urls import resolve, reverse


class RecipeViewsTest(TestCase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, home)

    def test_category_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(2,)))
        self.assertIs(view.func, category)

    def test_detail_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 10}))
        self.assertIs(view.func, recipe)

    def test_recipe_home_view_retuns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('no recipes found here', response.content.decode('utf-8'))
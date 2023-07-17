from .test_recipe_base import RecipeTestBase
from recipes import views
from django.urls import resolve, reverse
from unittest.mock import patch


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.Home)

    def test_recipe_home_view_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_load_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_show_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('no recipes found here', response.content.decode('utf-8')) # noqa

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Teste recipe is_published False don't show """

        # need a recipe for this test
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            'no recipes found here',
            response.content.decode('utf-8')
        )

    def test_category_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', args=(299999,)))
        self.assertIs(view.func.view_class, views.Category)

    def test_recipe_home_is_paginated(self): # noqa
        self.make_recipe_in_batch(qtd=9)

        # Mock sendo aplicado
        with patch('recipes.views.home_recipe.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)

    def test_invalid_page_query_uses_page_one(self):
        self.make_recipe_in_batch(qtd=8)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home') + '?page=1A')
            ...
            self.assertEqual(
                response.context['recipes'].number,
                1
            )


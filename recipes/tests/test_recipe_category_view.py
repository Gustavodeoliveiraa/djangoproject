from .test_recipe_base import RecipeTestBase
from django.urls import reverse
from unittest.mock import patch

class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_returns_status_code_404_if_no_recipes_found(self): # noqa
        response = self.client.get(
            reverse('recipes:category', args=(2999999,))
        )
        self.assertEqual(response.status_code, 404)

    def test_category_template_loads_recipes(self):
        self.make_recipe(title='this is a category test')

        response = self.client.get(reverse('recipes:category', args=(1,)))
        content = response.content.decode('utf-8')

        # Check if one recipe exists
        self.assertIn('this is a category test', content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Teste recipe is_published False don't show """

        # need a recipe for this test
        recipe = self.make_recipe(is_published=True)
        response = self.client.get(
            reverse(
                    'recipes:category',
                    args=(recipe.category.id,))  # type: ignore
            )

        self.assertEqual(response.status_code, 200)

    def test_recipe_category_is_paginated(self):
        # category needs to be out of loop because several category will has be created but with different names # noqa
        teste = self.make_category()
        for i in range(9):
            kwargs = {
                'author_data': {'username': f'u{i}'},
                'slug': f'r{i}',
            }
            self.make_recipe_with_same_category(category_data=teste, **kwargs)

        with patch('recipes.views.home_recipe.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 3)
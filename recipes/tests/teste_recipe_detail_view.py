from .test_recipe_base import RecipeTestBase
from recipes import views
from django.urls import resolve, reverse


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        self.assertIs(views.recipe, view.func)

    def test_recipe_detail_view_returns_404_if_no_recipes(self):
        response = self.client.get(
            reverse('recipes:recipe', args=(20000,))
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_the_correct_recipe(self):
        need_title = 'this is a detail page - it load one recipe'

        self.make_recipe(title=need_title)
        # need a recipe for this test

        response = self.client.get(reverse('recipes:recipe', args=(1,)))
        content = response.content.decode('utf-8')

        self.assertIn(need_title, content)

    def test_recipe_details_template_dont_load_recipes_not_published(self):
        """Teste recipe is_published False don't show """

        # need a recipe for this test
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe',
                    args=(recipe.id,))  # type: ignore
            )

        self.assertEqual(response.status_code, 404)


# from django.test import LiveServerTestCase aqui nao carrega arquivos estáticos  # noqa
from django.contrib.staticfiles.testing import StaticLiveServerTestCase # essa carrega arquivos estaticos no servidor  # noqa
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import RecipeBaseFunctionalTest
import pytest
from recipes.tests.test_recipe_base import RecipeMixin
from time import sleep
from unittest.mock import patch


@pytest.mark.functional_test  # pode ser usado na classe ou [...]
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest, RecipeMixin):

    # @pytest.mark.functional_test   [...]pode ser usando no teste em si
    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_home_page_without_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        # sleep(5)
        self.assertIn('no recipes found here', body.text)

    @patch('recipes.views.PER_PAGE', new=9)
    def test_recipe_search_input_can_find_correct_recipe(self):
        recipes = self.make_recipe_in_batch()
        # User open browser
        self.browser.get(self.live_server_url)

        # See a search field input
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Search for a recipe"]'
        )

        # click on this input and type the term of search
        # "Recipe title 1" for search a recipe with this title
        search_input.send_keys(recipes[0].title)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            recipes[0].title,
            self.browser.find_element(By.TAG_NAME, "body").text
        )

        sleep(4)

    @patch('recipes.views.home_recipe.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # user open the page
        self.browser.get(self.live_server_url)

        # See that there is pagination and click on page 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )

        page2.click()

        # See that there is more two recipes in page 2

        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, "recipe")),
            2
        )


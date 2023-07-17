from .base import AuthorBaseTest
import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=string_password 
        )
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(user.username)
        password.send_keys(string_password)
        form.submit()
        self.assertIn(
            'You are logged in',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_invalid_data_can_login_successfully(self):
        self.browser.get(self.live_server_url + reverse('authors:login'))
        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )
        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys('user')
        password.send_keys('password')
        form.submit()
        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_created_raise_404_if_not_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_form_login_is_invalid(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login')
        )
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/div[2]/form'
        )

        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')
        username.send_keys(' ')
        password.send_keys(' ')

        form.submit()

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(
                By.TAG_NAME, 'body'
            ).text
        )

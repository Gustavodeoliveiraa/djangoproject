from .base import AuthorBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorBaseTest):
    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )
    
    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()

        self.fill_form_dummy_data(form)

        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form

    def test_empty_first_name_empty(self):
        def callback(form):
            first_name = self.get_by_placeholder(form, "Ex: John")
            first_name.send_keys(' ')
            first_name.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_empty(self):
        def callback(form):
            last_name = self.get_by_placeholder(form, "Ex: Doe")
            last_name.send_keys(' ')
            last_name.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_empty(self):
        def callback(form):
            username = self.get_by_placeholder(form, "Your Username")
            username.send_keys(' ')
            username.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('This field must not be empty', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, "Your E-Mail")
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()

            self.assertIn('The e-mail must be valid', form.text)
        self.form_field_test_with_callback(callback)

    def test_password_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, "Your password")
            password2 = self.get_by_placeholder(form, "Repeat your password")
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_dif')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Password and password2 must be equal', form.text)
        self.form_field_test_with_callback(callback)

    #falhando
    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register')
        form = self.get_form()

        self.get_by_placeholder(form, "Ex: John").send_keys('First Name')
        self.get_by_placeholder(form, "Ex: Doe").send_keys('Last Name')
        self.get_by_placeholder(form, "Your Username").send_keys('my_username1')
        self.get_by_placeholder(form, "Your E-Mail").send_keys('emaill@gmail.com') # noqa
        self.get_by_placeholder(form, "Your password").send_keys('Abc@12345678910')
        self.get_by_placeholder(form, "Repeat your password").send_keys('Abc@12345678910') # noqa
        form.submit()

        self.assertIn(
            'Your user is created',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
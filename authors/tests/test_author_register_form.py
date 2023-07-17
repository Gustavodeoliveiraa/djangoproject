from django.test import TestCase as DjangoTestCase
from unittest import TestCase

from authors.forms import RegisterForm
from parameterized import parameterized

from django.urls import reverse


class AuthorRegisterForm(TestCase):
    @parameterized.expand([
        ('username', 'Your Username'),
        ('email', 'Your E-Mail'),
        ('first_name', 'Ex: John'),
        ('last_name', 'Ex: Doe'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('username', 'Username must have letter, number or one of those @.+-_ '
            'The length should be between 4 and 150 characters'),
        ('email', 'The e-mail must be valid'),
        ('password', 'Password must have at least one uppercase letter '
            'one lowercase latter and one number. the length should be '
            'at least 8 characters'),
    ])
    def test_fields_help_texts_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('password', 'Password'),
        ('password2', 'Password'),
    ])
    def test_label_field_is_correct(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)

    @parameterized.expand([
            ('email', 'The e-mail must be valid'),
            ('password', 'Password must have at least one uppercase letter '
                'one lowercase latter and one number. the length should be '
                'at least 8 characters'),
    ])
    def test_help_text_fields_is_correct(self, field, text_field):
        form = RegisterForm()
        current = form[field].help_text
        self.assertEqual(current, text_field)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'This field must not be empty'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Password must not be empty'),
        ('email', 'E-mail is required')
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        msg = 'Username must have at least 4 characters'
        self.form_data['username'] = 'joo'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        msg = 'Username must have less than 150 characters'
        self.form_data['username'] = 'a' * 152
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        # self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_case_letters_and_numbers(self):
        self.form_data['password'] = 'abc123'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password must have at least one uppercase letter one lowercase latter and one number. the length should be at least 8 characters' # noqa

        self.assertIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_is_equal(self):
        self.form_data['password'] = 'Str0ngP@ssword1'
        self.form_data['password2'] = 'Str0ngP@ssword10'

        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Password and password2 must be equal'
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_create_views_returns_404(self):
        self.form_data['password'] = 'Str0ngP@ssword1'
        self.form_data['password2'] = 'Str0ngP@ssword10'

        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'User e-mail is already in use'

        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def teste_author_created_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'testeuser',
            'password': '@Bc123456',
            'password2': '@Bc123456',
        })
        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testeuser',
            password='@Bc123456'
        )

        self.assertTrue(is_authenticated)

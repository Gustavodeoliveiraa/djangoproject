from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Your Username')
        add_placeholder(self.fields['email'], 'Your E-Mail')
        add_placeholder(self.fields['first_name'], 'Ex: John')
        add_placeholder(self.fields['last_name'], 'Ex: Doe')
        add_placeholder(self.fields['password'], 'Your password')
        add_placeholder(self.fields['password2'], 'Repeat your password')

    username = forms.CharField(
        label='Username',
        help_text=(
            'Username must have letter, number or one of those @.+-_ '
            'The length should be between 4 and 150 characters'
        ), # noqa
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters'
            },
        min_length=4, max_length=150
    )

    password2 = forms.CharField(
        error_messages={'required': 'Password must not be empty'},
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        label='Password'
    )

    password = forms.CharField(
        error_messages={'required': 'Password must not be empty'},
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Your password'
        }),
        help_text='Password must have at least one uppercase letter '
            'one lowercase latter and one number. the length should be '
            'at least 8 characters',
        validators=[strong_password],
        label='Password'

    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )

    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid',
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]  # select the fields they i can want

        
        #  se precisar de coisas bem especificas é nescessario sobrescrever o widgets  do camposa # noqa
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Type your username here',
                'class': 'input text-input outra-classe'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type your password here',
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exist = User.objects.filter(email=email).exists()

        if exist:
            raise ValidationError(
                'User e-mail is already in use', code='invalid')

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError({
                'password': 'Password and password2 must be equal',
                'password2': 'Password and password2 must be equal',
             })
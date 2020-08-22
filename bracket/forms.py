from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Sign Up Form
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
        ]

class LoginForm(AuthenticationForm):
    username = forms.EmailField()

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields['username'].label = 'Email'
        self.fields['username'].verbose_name = 'email'

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(mark_safe("Please confirm your email before signing in", code='unconfirmed'))

        super().confirm_login_allowed(user)

    @property
    def helper(self):
        helper = FormHelper(self)
        helper.form_tag = False
        helper.use_custom_control = False

        return helper
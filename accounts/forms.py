from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm, LoginForm

User = get_user_model()


class CustomSignupForm(SignupForm):
    """Custom signup form for allauth."""
    
    first_name = forms.CharField(
        max_length=30,
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'class': 'input input-bordered w-full',
            }
        )
    )
    
    last_name = forms.CharField(
        max_length=30,
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name',
                'class': 'input input-bordered w-full',
            }
        )
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'input input-bordered w-full',
            }
        )
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '••••••••',
                'class': 'input input-bordered w-full',
            }
        )
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '••••••••',
                'class': 'input input-bordered w-full',
            }
        )
    )
    
    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user


class CustomLoginForm(LoginForm):
    """Custom login form for allauth."""
    
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '••••••••',
                'class': 'input input-bordered w-full',
            }
        )
    )
    
    login = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email Address',
                'class': 'input input-bordered w-full',
                'autofocus': 'autofocus',
            }
        )
    )
    
    remember = forms.BooleanField(
        label='Remember Me',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox checkbox-primary',
            }
        )
    )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'profile_picture', 'bio', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'last_name': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'email': forms.EmailInput(attrs={'class': 'input input-bordered w-full'}),
            'bio': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 4}),
            'phone_number': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'profile_picture': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
        }

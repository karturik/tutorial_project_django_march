from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        # Указываем поля, которые должны быть в форме
        fields = ['name', 'email', 'message'] 
        # Можно добавить виджеты для настройки полей ввода, если нужно
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}), 
        }

# Create your forms here.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Profile
from .utils import normalize_phone

class BaseAccountForm(forms.ModelForm):
    email = forms.EmailField(label='Имейл', max_length=254, required=True)
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=True,
        help_text='Въведете 9 цифри без +359 и без начална 0.',
        widget=forms.TextInput(attrs={
            'type': 'tel',
            'placeholder': '888 888 888',
        }),
    )


    company = forms.CharField(label='Фирма', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

        self.fields['first_name'].label = 'Име'
        self.fields['last_name'].label = 'Фамилия'

    def clean_phone(self):
        phone = normalize_phone(self.cleaned_data.get('phone', ''))


        if Profile.objects.filter(phone=phone).exclude(
            user_id=self.instance.pk,
        ).exists():
            raise forms.ValidationError(
                'Вече съществува акаунт с този телефон.'
            )

        return phone



class RegistrationForm(UserCreationForm, BaseAccountForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.pop('autofocus', None)
        self.fields['first_name'].widget.attrs['autofocus'] = True

        self.fields['username'].label = 'Потребителско име'


class ProfileForm(BaseAccountForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


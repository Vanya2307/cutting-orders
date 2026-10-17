import re

from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone', 'email', 'company']

        labels = {
            'name': 'Име',
            'phone': 'Телефон',
            'email': 'Имейл',
            'company': 'Фирма',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Например: Петър Петров'}
            ),
            'phone': forms.TextInput(
                attrs={
                    'type': 'tel',
                    'placeholder': 'Например: 888 888 888',
                    'autocomplete': 'tel',
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Например: pepi@example.com',
                    'autocomplete': 'email',
                }
            )
        }

        help_texts = {
            'phone': 'Въведете 9 цифри без +359 и без начална 0.',
        }

        error_messages = {
            'name': {
                'required': 'Моля, въведете Вашето име.',
            },
            'phone': {
                'required': 'Моля, въведете Вашия телефонен номер.',
            },
            'email': {
                'invalid': 'Моля, въведете валиден имейл адрес.'
            }
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '')

        phone = re.sub(r'[\s()-]', '', phone)

        if phone.startswith('+359'):
            phone = phone[4:]


        if phone.startswith('0'):
            phone = phone[1:]

        if not re.fullmatch(r'[0-9]{9}', phone):
            raise forms.ValidationError(
                'Моля, въведете валиден български мобилен номер.'
            )


        return f'+359{phone}'


    def validate_unique(self):
        # Allow existing phones; order creation must reuse their Client.
        pass


    def clean(self):
        cleaned_data = super().clean()
        self.matching_client = None

        name = cleaned_data.get('name')
        phone = cleaned_data.get('phone')

        if not name or not phone:
            return cleaned_data

        client = Client.objects.filter(phone=phone).first()

        if client:
            input_name = " ".join(name.split()).lower()

            db_name = " ".join(client.name.split()).lower()

            if input_name != db_name:
                raise forms.ValidationError(
                    'Проверете въведените име и телефонен номер.'
                )

            self.matching_client = client

        return cleaned_data


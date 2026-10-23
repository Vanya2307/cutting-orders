import re

from django import forms
from .models import Client, Detail, OrderDrawing

from django.core.validators import FileExtensionValidator

from catalog.models import Material


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




class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail

        fields = [
            'material',
            'name',
            'length',
            'width',
            'quantity',
            'grain_direction',
            'edge_l_top',
            'edge_l_bottom',
            'edge_w_left',
            'edge_w_right',
            'euro_joint_left',
            'euro_joint_right',
            'services',
            'other',
            'processing',
        ]

        labels = {
            'material': 'Материал',
            'name': 'Наименование на детайла (по желание)',
            'length': 'Дължина L, мм',
            'width': 'Ширина W, мм',
            'quantity': 'Количество, бр.',
            'grain_direction': 'Посока на фладера',
            'edge_l_top': 'Кант L горе, мм',
            'edge_l_bottom': 'Кант L долу, мм',
            'edge_w_left': 'Кант W ляво, мм',
            'edge_w_right': 'Кант W дясно, мм',
            'euro_joint_left': 'Евросглобка, лява',
            'euro_joint_right': 'Евросглобка, дясна',
            'services': 'Обработки',
            'processing': 'Уточнение към обработките',
            'other': 'Друго',
        }


        help_texts = {
            'services': 'Изберете необходимите обработки.',
            'processing': 'Например: разстояние между отворите за панти.',
            'other': 'Например: кант в различен цвят, сдвоени детайли.',
        }


        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Например: Страница, Дъно, Врата...'}
            ),
            'services': forms.CheckboxSelectMultiple(),
            'processing': forms.Textarea(
                attrs={'rows': 2}
            ),
            'other': forms.Textarea(
                attrs={'rows': 2}
            ),
            'grain_direction': forms.RadioSelect(),
        }

        error_messages = {
            'material': {
                'required': 'Моля, изберете материал.',
                'invalid_choice': 'Моля, изберете материал от списъка.',
            },
            'name': {
                'max_length': 'Наименованието може да е до 100 символа.',
            },
            'length': {
                'required': 'Моля, въведете дължина.',
                'invalid': 'Моля, въведете цяло число.',
                'min_value': 'Минималната дължина е 18 мм.',
            },
            'width': {
                'required': 'Моля, въведете ширина.',
                'invalid': 'Моля, въведете цяло число.',
                'min_value': 'Минималната ширина е 18 мм.',
            },
            'quantity': {
                'required': 'Моля, въведете количество.',
                'invalid': 'Моля, въведете цяло число.',
                'min_value': 'Количеството трябва да бъде поне 1.',
            },
            'grain_direction': {
                'required': 'Моля, изберете посока на фладера.',
            },
            'processing': {
                'max_length': 'Уточнението може да е до 255 символа.',
            },
            'other': {
                'max_length': 'Текстът може да е до 255 символа.',
            },
        }


    def __init__(self, *args, material=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['grain_direction'].choices = Detail.DIRECTION_CHOICES
        self.fields['material'].empty_label = 'Изберете материал'
        self.fields['grain_direction'].required = False
        self.selected_material = None

        if material is None and self.instance.material_id:
            material = self.instance.material

        if material is not None:
            self.fields['material'].queryset = Material.objects.filter(
                pk=material.pk
            )
            self.initial['material'] = material.pk
            self.fields['material'].disabled = True
            self.fields['material'].empty_label = None
            self.selected_material = material


class OrderDrawingForm(forms.ModelForm):
    class Meta:
        model = OrderDrawing
        fields = ['file']
        labels = {'file': 'Чертеж'}
        widgets = {'file': forms.ClearableFileInput(attrs={'accept': '.pdf, .jpg, .jpeg, .png'})}
        help_texts = {'file': 'Допустими формати: PDF, JPG и PNG. Максимален размер: 5 MB.'}
        error_messages = {'file': {'required': 'Моля, изберете файл с чертеж.'}}

    def clean_file(self):
        file = self.cleaned_data['file']

        validate_extension = FileExtensionValidator(
            allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'],
            message='Моля, изберете PDF, JPG или PNG файл.'
        )

        validate_extension(file)

        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError('Размерът на файла не трябва да надвишава 5 MB.')

        return file


class OrderSubmitForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label='Проверих всички размери, кантове и обработки.',
        error_messages={
            'required': 'Моля, потвърдете, че сте проверили поръчката.',
        },
    )

    def __init__(self, *args, order, **kwargs):
        super().__init__(*args, **kwargs)
        self.order = order

    def clean(self):
        cleaned_data = super().clean()

        if not self.order.details.exists():
            raise forms.ValidationError('Добавете поне един детайл, преди да изпратите поръчката.')

        drawing_required = self.order.details.filter(services__drawing_requirement='REQUIRED').exists()

        if drawing_required and not self.order.drawings.exists():
            raise forms.ValidationError(
                'Избрана е обработка със задължителен чертеж. '
                'Моля, качете чертеж към поръчката.'
            )

        return cleaned_data




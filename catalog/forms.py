from django import forms
from .models import Material, Service


class ThicknessInput(forms.NumberInput):
    def format_value(self, value):
        value = super().format_value(value)

        if value is not None:
            return value.removesuffix('.0')

        return value

    
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            'material_type',
            'manufacturer',
            'decor_code',
            'decor_name',
            'board_length',
            'board_width',
            'thickness',
            'has_grain',
        ]

        labels = {
            'material_type': 'Тип',
            'manufacturer': 'Производител',
            'decor_code': 'Код на декора',
            'decor_name': 'Име на декора',
            'thickness': 'Дебелина, мм',
            'board_length': 'Дължина на плочата, мм',
            'board_width': 'Ширина на плочата, мм',
            'has_grain': 'Фладер',
        }

        widgets = {
            'decor_code': forms.TextInput(
                attrs={'placeholder': 'Например: 5981 HG'}
            ),
            'decor_name': forms.TextInput(
                attrs={'placeholder': 'Например: Кашмир Гланц'}
            ),
            'thickness': ThicknessInput(),
        }

        help_texts = {
            'decor_code': 'За Фазер въведете цвят, например Бял.',
            'has_grain': 'Отбележете, ако декорът има шарка с посока.',
        }

        error_messages = {
            'decor_code': {
                'required': 'Въведете код на декора или цвят на фазер.',
                'max_length': 'Най-много 20 символа.'
            },
            'decor_name': {
                'required': 'Въведете наименование на декора.',
                'max_length': 'Най-много 100 символа.'
            },
            'thickness': {
                'required': 'Въведете дебелина на материала.'
            },

            'board_length': {
                'required': 'Въведете дължина на плочата.'
            },
            'board_width': {
                'required': 'Въведете ширина на плочата.'
            },
            'material_type': {
                'required': 'Изберете тип на материала.',
            },
            'manufacturer': {
                'required': 'Изберете производител.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['material_type'].choices = [('', 'Изберете материал…'), *Material.TYPE_CHOICES,]
        self.fields['manufacturer'].choices = [('', 'Изберете производител…'),*Material.MANUFACTURER_CHOICES,]


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'drawing_requirement']

        labels = {
            'name': 'Наименование на услугата',
            'drawing_requirement': 'Изискване за чертеж',
        }

        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': 'Например: Отвори за панти'}
            ),
            'drawing_requirement': forms.RadioSelect(),
        }

        help_texts = {
            'drawing_requirement': 'Посочете дали клиентът трябва да прикачи чертеж за тази услуга.',
        }

        error_messages = {
            'name': {
                'required': 'Въведете име на услугата.',
                'unique': 'Услуга с това име вече съществува.',
                'max_length': 'Името може да е до 100 символа',
            },
            'drawing_requirement': {
                'required': 'Изберете опция за чертеж.',
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['drawing_requirement'].choices = Service.DRAWING_CHOICES




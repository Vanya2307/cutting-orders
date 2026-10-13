from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Material(models.Model):
    TYPE_CHOICES = [
        ('LPDCH', 'ЛПДЧ'),
        ('MDF', 'MDF'),
        ('HDF', 'Фазер'),
        ('TOP', 'Плот'),
        ('BACK', 'Гръб'),
    ]
    MANUFACTURER_CHOICES = [
        ('EGGER', 'Egger'),
        ('KRONOSPAN', 'Кроношпан'),
        ('FUNDERMAX', 'Fundermax'),
        ('SALEX', 'Салекс'),
        ('KASTAMONU', 'Кастамону'),
        ('AGT', 'AGT'),
        ('YILDIZ', 'YILDIZ'),
        ('EVOGLOSS', 'Evogloss'),
        ('GETALIT', 'Getalit'),
        ('GLUNZ', 'Glunz')
    ]
    BOARD_SIZES = {
        'LPDCH': {'length': 2800, 'widths': [2070]},
        'MDF': {'length': 2800, 'widths': [1300, 1220]},
        'HDF': {'length': 2800, 'widths': [2070]},
        'TOP': {'length': 4100, 'widths': [600, 635, 920]},
        'BACK': {'length': 4100, 'widths': [620, 640]},
    }
    material_type = models.CharField(max_length=5, choices=TYPE_CHOICES)
    manufacturer = models.CharField(max_length=50, choices=MANUFACTURER_CHOICES)

    decor_code = models.CharField(max_length=20)
    decor_name = models.CharField(max_length=100)

    thickness = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(3)])
    board_length = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    board_width = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    has_grain = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.decor_code} {self.decor_name}"

    def clean(self):
        super().clean()

        board_size = self.BOARD_SIZES.get(self.material_type)

        if board_size is None:
            return

        errors = {}
        if self.board_length is not None and self.board_length != board_size['length']:
            errors['board_length'] = (
                f"Дължината на плочата трябва да бъде {board_size['length']} мм."
            )

        if self.board_width is not None and self.board_width not in board_size['widths']:
            allowed_widths = ', '.join(str(w) for w in board_size['widths'])
            errors['board_width'] = (
                f"Допустими ширини: {allowed_widths} мм."
            )

        if errors:
            raise ValidationError(errors)


    class Meta:
        ordering = ['material_type', 'decor_code']
        verbose_name = 'Материал'
        verbose_name_plural = 'Материали'
    
        constraints = [
            models.UniqueConstraint(
                fields=[
                    'material_type',
                    'manufacturer',
                    'decor_code',
                    'thickness',
                    'board_length',
                    'board_width',
                ],
                name='unique_material_variant',
                violation_error_message='Този материал вече съществува.',
            ),
        ]


class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)
    DRAWING_CHOICES = [
        ('NONE', 'Без чертеж'),
        ('RECOMMENDED', 'Препоръчителен'),
        ('REQUIRED', 'Задължителен'),

    ]
    drawing_requirement = models.CharField(max_length=15, choices=DRAWING_CHOICES)

    def __str__(self):
        return self.name


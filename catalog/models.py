from django.db import models
from django.core.validators import MinValueValidator


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


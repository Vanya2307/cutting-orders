from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError


class Client(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
    company = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Чернова'),
        ('SUBMITTED', 'Изпратена')
    ]
    
    
    client = models.ForeignKey(
        "orders.Client",
        on_delete=models.PROTECT,
        related_name="orders",
    )

    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField(blank=True)
    contact_company = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')
    number = models.CharField(max_length=30, unique=True, blank=True, null=True)
    excel_file = models.FileField(blank=True, upload_to='orders/excel/')

    def __str__(self):
        if self.number:
            return self.number
        return f"{self.get_status_display()} #{self.pk} - {self.client.name}"


class Detail(models.Model):
    DIRECTION_CHOICES = [
        ('L', 'По дължина L'),
        ('W', 'По ширина W'),
        ('ANY', 'Без значение'),
    ]
    THICKNESS_CHOICES = [
        (Decimal('0.0'), 'Без кант'),
        (Decimal('0.5'), '0.5'),
        (Decimal('0.8'), '0.8'),
        (Decimal('1.0'), '1'),
        (Decimal('2.0'), '2'),
    ]
    JOINT_CHOICES = [
        ('NO_JOINT', 'Без сглобка'),
        ('MAIN', 'Основен'),
        ('JOINING', 'Присъединителен'),
    ]
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="details",
    )
    material = models.ForeignKey(
        "catalog.Material",
        on_delete=models.PROTECT,
        related_name="details",
    )
    name = models.CharField(max_length=100, blank=True)
    length = models.PositiveIntegerField(validators=[MinValueValidator(18)])
    width = models.PositiveIntegerField(validators=[MinValueValidator(18)])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    services = models.ManyToManyField("catalog.Service", blank=True)
    grain_direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES)

    edge_l_top = models.DecimalField(max_digits=2, decimal_places=1, choices=THICKNESS_CHOICES, default=0)
    edge_l_bottom = models.DecimalField(max_digits=2, decimal_places=1, choices=THICKNESS_CHOICES, default=0)
    edge_w_left = models.DecimalField(max_digits=2, decimal_places=1, choices=THICKNESS_CHOICES, default=0)
    edge_w_right = models.DecimalField(max_digits=2, decimal_places=1, choices=THICKNESS_CHOICES, default=0)

    euro_joint_left = models.CharField(max_length=30, choices=JOINT_CHOICES, default='NO_JOINT')
    euro_joint_right = models.CharField(max_length=30, choices=JOINT_CHOICES, default='NO_JOINT')

    other = models.CharField(max_length=255, blank=True)
    processing = models.CharField(max_length=255, blank=True)


    def __str__(self):
        if self.name:
            return f"{self.name} - {self.length}/{self.width} - {self.quantity}"
        return f"{self.length}/{self.width} - {self.quantity}"


    def clean(self):
        super().clean()

        if not self.material_id:
            return


        errors = {}

        if not self.material.has_grain:
            self.grain_direction = 'ANY'
        elif not self.grain_direction:
            errors['grain_direction'] = (
                'Моля, изберете посока на фладера или "Без значение".'
            )
        

        

        for field_name in ('euro_joint_left', 'euro_joint_right'):
            joint = getattr(self, field_name)

            if joint != 'NO_JOINT':
                if self.material.material_type != 'TOP':
                    errors[field_name] = ('Евросглобката е възможна само при плот.')
                elif self.width is not None and self.width != 600:
                    errors['width'] = (
                        'Стандартната евросглобка е за ширина 600 мм. '
                        'За друга ширина, моля, свържете се с нас.'
                    )
       

        usable_length, usable_width = self.material.usable_size()

        fits_lengthwise = (
            (self.length is None or self.length <= usable_length)
            and (self.width is None or self.width <= usable_width)
        )

        fits_rotated = (
            (self.width is None or self.width <= usable_length)
            and (self.length is None or self.length <= usable_width)
        )

        if self.grain_direction == 'L':
            fits = fits_lengthwise
        elif self.grain_direction == 'W':
            fits = fits_rotated
        else:
            fits = fits_lengthwise or fits_rotated

        if not fits:
            errors[NON_FIELD_ERRORS] = (
                'Детайлът не се побира в плочата при избраната посока. '
                'Чист размер след окрайчване: '
                f'{usable_length} × {usable_width} мм.'
            )

        if errors:
            raise ValidationError(errors)



class OrderDrawing(models.Model):
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="drawings",
    )
    file = models.FileField(upload_to="orders/drawings/")

    def __str__(self):
        return self.file.name


from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

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
        (Decimal('0'), 'Без кант'),
        (Decimal('0.5'), '0.5мм'),
        (Decimal('0.8'), '0.8мм'),
        (Decimal('1'), '1мм'),
        (Decimal('2'), '2мм'),
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



class OrderDrawing(models.Model):
    order = models.ForeignKey(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="drawings",
    )
    file = models.FileField(upload_to="orders/drawings/")

    def __str__(self):
        return self.file.name


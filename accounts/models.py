from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile', 
        verbose_name='Потребител',
    )
    phone = models.CharField(max_length=20, unique=True, verbose_name='Телефон')

    company = models.CharField(max_length=100, blank=True, verbose_name='Фирма')
    
    favourite_materials = models.ManyToManyField(
        'catalog.Material', 
        blank=True, 
        related_name='favourited_by', 
        verbose_name='Любими материали',
    )

    class Meta:
        verbose_name = 'Профил'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профил на {self.user.username}"

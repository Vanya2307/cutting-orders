from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'company')

    search_fields = ('user__username', 'user__email', 'phone', 'company')

    filter_horizontal = ('favourite_materials',)
    list_select_related = ('user',)


from django.contrib import admin
from .models import Material, Service

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'decor_code', 
        'decor_name', 
        'material_type', 
        'manufacturer', 
        'thickness', 
        'board_length',
        'board_width',
        'has_grain',
    )

    list_filter = ('material_type', 'manufacturer', 'has_grain')
    search_fields = ('decor_code', 'decor_name')



@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'drawing_requirement')
    list_filter = ('drawing_requirement',)
    search_fields = ('name',)
    actions = None

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.detail_set.exists():
            return False
        
        return super().has_delete_permission(request, obj)

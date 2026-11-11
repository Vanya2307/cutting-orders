from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError

from django.db import transaction

GROUP_PERMISSIONS = {
    'Клиенти': (
        'catalog.view_material', 
        'catalog.view_service',
    ),
    'Цех': (
        'catalog.view_material',
        'catalog.add_material',
        'catalog.change_material',
        'catalog.delete_material',
        'catalog.view_service',
        'catalog.add_service',
        'catalog.change_service',
        'catalog.delete_service',
    ),
}

class Command(BaseCommand):
    help = 'Създава групите и обновява правата им за достъп.'

    def handle(self, *args, **options):

        with transaction.atomic():
            for group_name, full_permission_names in GROUP_PERMISSIONS.items():
                permission_objects = []

                for full_name in full_permission_names:
                    app_label, codename = full_name.split('.', 1)

                    try:
                        permission = Permission.objects.get(
                            content_type__app_label=app_label,
                            codename=codename
                        )
                        permission_objects.append(permission)
                    except Permission.DoesNotExist:
                        raise CommandError(
                            f'Не е намерено право за достъп: {full_name}. '
                            'Първо изпълнете python manage.py migrate.'
                        )
                group, _ = Group.objects.get_or_create(name=group_name)

                group.permissions.set(permission_objects)

        self.stdout.write(
            self.style.SUCCESS('Групите и правата за достъп са настроени успешно.')
        )
                    

       
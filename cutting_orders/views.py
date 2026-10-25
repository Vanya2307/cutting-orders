
from django.shortcuts import render
from catalog.models import Material, Service


def home(request):

    context = {
        'materials_count': Material.objects.count(),
        'services_count': Service.objects.count(),
    }

    return render(request, "home.html", context)
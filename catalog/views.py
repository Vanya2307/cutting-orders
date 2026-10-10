from django.shortcuts import render

from django.views.generic import ListView, DetailView
from .models import Material

class MaterialListView(ListView):
    model = Material
    template_name = "catalog/material_list.html"
    context_object_name = "materials"


class MaterialDetailView(DetailView):
    model = Material
    template_name = "catalog/material_detail.html"
    context_object_name = "material"
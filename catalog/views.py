
from django.views.generic import ListView, DetailView, CreateView
from .models import Material
from .forms import MaterialForm
from django.urls import reverse_lazy

class MaterialListView(ListView):
    model = Material
    template_name = "catalog/material_list.html"
    context_object_name = "materials"


class MaterialDetailView(DetailView):
    model = Material
    template_name = "catalog/material_detail.html"
    context_object_name = "material"


class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = 'catalog/material_form.html'
    success_url = reverse_lazy('catalog:material-list')
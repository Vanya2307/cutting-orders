
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Material
from .forms import MaterialForm
from django.urls import reverse_lazy, reverse

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


class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = 'catalog/material_form.html'

    def get_success_url(self):
        return reverse('catalog:material-detail', kwargs={'pk': self.object.pk})


class MaterialDeleteView(DeleteView):
    model = Material
    template_name = 'catalog/material_confirm_delete.html'
    success_url = reverse_lazy('catalog:material-list')

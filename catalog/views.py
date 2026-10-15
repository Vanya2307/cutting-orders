
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Material, Service
from .forms import MaterialForm, ServiceForm
from django.urls import reverse_lazy, reverse

from django.db.models.deletion import ProtectedError

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

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            form.add_error(None, 'Този материал не може да бъде изтрит, използва се в заявка.')

            return self.form_invalid(form)


class ServiceListView(ListView):
    model = Service
    template_name = "catalog/service_list.html"
    context_object_name = "services"


class ServiceDetailView(DetailView):
    model = Service
    template_name = "catalog/service_detail.html"
    context_object_name = "service"


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'
    success_url = reverse_lazy('catalog:service-list')


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'catalog/service_form.html'

    def get_success_url(self):
        return reverse('catalog:service-detail', kwargs={'pk': self.object.pk})



class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'catalog/service_confirm_delete.html'
    success_url = reverse_lazy('catalog:service-list')

    def form_valid(self, form):
        if self.object.detail_set.exists():
            form.add_error(
                None,
                'Тази услуга не може да бъде изтрита, защото се използва в заявка.'
            )
            return self.form_invalid(form)

        return super().form_valid(form)
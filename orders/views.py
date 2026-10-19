from pathlib import Path

from django.http import FileResponse
from django.views import View

from django.views.generic import CreateView, FormView, DetailView, UpdateView, DeleteView
from .forms import ClientForm, DetailForm, OrderDrawingForm

from .models import Order, Detail, OrderDrawing
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from django.db import transaction

class OrderCreateView(FormView):
    form_class = ClientForm
    template_name = 'orders/order_form.html'

    def form_valid(self, form):
        data = form.cleaned_data

        with transaction.atomic():
            client = getattr(form, 'matching_client', None)

            if client is None:
                client = form.save()

            order = Order.objects.create(
                client=client,
                contact_name=data['name'],
                contact_phone=data['phone'],
                contact_email=data['email'],
                contact_company=data['company'],
            )

        order_ids = self.request.session.get('order_ids', [])
        order_ids.append(order.pk)
        self.request.session['order_ids'] = order_ids

        return redirect('orders:order-detail', pk=order.pk)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        order_ids = self.request.session.get('order_ids', [])
        
        return super().get_queryset().filter(pk__in=order_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ordered_details = (
            self.object.details
            .select_related('material')
            .order_by('material__decor_code', 'material_id', 'pk')
        )
        context['details'] = ordered_details
        return context

class DraftDetailMixin:
    def get_queryset(self):
        order_ids = self.request.session.get('order_ids', [])

        return super().get_queryset().filter(
            order_id=self.kwargs['order_pk'],
            order_id__in=order_ids,
            order__status='DRAFT',
        )


class DraftOrderMixin:
    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(
            Order,
            pk=kwargs['order_pk'],
            pk__in=request.session.get('order_ids', []),
            status='DRAFT',
        )
        return super().dispatch(request, *args, **kwargs)




class DetailCreateView(DraftOrderMixin, CreateView):
    model = Detail
    form_class = DetailForm
    template_name = 'orders/detail_form.html'


    def form_valid(self, form):
        form.instance.order = self.order

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'orders:order-detail',
            kwargs={'pk': self.order.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order

        return context

class DetailUpdateView(DraftDetailMixin, UpdateView):
    model = Detail
    form_class = DetailForm
    template_name = 'orders/detail_form.html'


    def get_success_url(self):
        return reverse(
            'orders:order-detail',
            kwargs={'pk': self.object.order_id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object.order

        return context


class DetailDeleteView(DraftDetailMixin, DeleteView):
    model = Detail
    template_name = 'orders/detail_confirm_delete.html'

    def get_success_url(self):
        return reverse(
            'orders:order-detail',
            kwargs={'pk': self.object.order_id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object.order

        return context


class OrderDrawingCreateView(DraftOrderMixin, CreateView):
    model = OrderDrawing
    form_class = OrderDrawingForm
    template_name = 'orders/order_drawing_form.html'


    def form_valid(self, form):
        form.instance.order = self.order

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'orders:order-detail',
            kwargs={'pk': self.order.pk},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order

        return context


class OrderDrawingDownloadView(View):
    def get(self, request, order_pk, pk):
        drawing = get_object_or_404(
            OrderDrawing,
            pk=pk,
            order_id=order_pk,
            order_id__in=request.session.get('order_ids', []),
        )

        return FileResponse(
            drawing.file.open('rb'),
            as_attachment=False,
            filename=Path(drawing.file.name).name,
        )



class OrderDrawingDeleteView(DraftDetailMixin, DeleteView):
    model = OrderDrawing
    template_name = 'orders/order_drawing_confirm_delete.html'

    def form_valid(self, form):
        self.object.file.delete(save=False)
        return super().form_valid(form)


    def get_success_url(self):
        return reverse(
            'orders:order-detail',
            kwargs={'pk': self.object.order_id},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object.order
        return context

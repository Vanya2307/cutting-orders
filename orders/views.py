from io import BytesIO

from django.core.files.base import ContentFile
from production.excel import generate_order_excel

from pathlib import Path

from django.http import FileResponse, Http404
from django.views import View

from django.views.generic import CreateView, FormView, DetailView, ListView, UpdateView, DeleteView
from .forms import ClientForm, DetailForm, OrderDrawingForm, OrderSubmitForm

from .models import Order, Detail, OrderDrawing
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from django.db import IntegrityError, transaction
from django.utils import timezone

from catalog.forms import MaterialFilterForm
from catalog.models import Material

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
            .prefetch_related('services')
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


class OrderSubmitView(DraftOrderMixin, FormView):
    form_class = OrderSubmitForm
    template_name = 'orders/order_confirm_submit.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['order'] = self.order

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order

        context['details'] = (
            self.order.details
            .select_related('material')
            .prefetch_related('services')
            .order_by('material__decor_code', 'material_id', 'pk')
        )

        context['drawing_recommended'] = (
            not self.order.drawings.exists()
            and self.order.details.filter(services__drawing_requirement='RECOMMENDED').exists()
        )
        return context

    def form_valid(self, form):
        submitted_at = timezone.now()
        year = timezone.localtime(submitted_at).year
        saved_file_name = None

        try:
            with transaction.atomic():
                updated = Order.objects.filter(
                    pk=self.order.pk,
                    status='DRAFT',
                ).update(
                    status='SUBMITTED',
                    submitted_at=submitted_at,
                )

                if not updated:
                    return redirect('orders:order-detail', pk=self.order.pk)

                self.order.refresh_from_db()
                self.order.number = Order.next_number(year)

                workbook = generate_order_excel(self.order)

                with BytesIO() as buffer:
                    workbook.save(buffer)

                    self.order.excel_file.save(
                        f'{self.order.number}.xlsx',
                        ContentFile(buffer.getvalue()),
                        save=False,
                    )

                saved_file_name = self.order.excel_file.name

                self.order.save(
                    update_fields=['number', 'excel_file'],
                )

        except (IntegrityError, OSError):
            if saved_file_name:
                self.order.excel_file.storage.delete(saved_file_name)

            self.order.refresh_from_db()

            form.add_error(None, 'Поръчката не беше изпратена. Моля, опитайте отново.')
            return self.form_invalid(form)

        return redirect('orders:order-detail', pk=self.order.pk)



class MaterialSelectView(DraftOrderMixin, ListView):
    model = Material
    template_name = 'orders/material_select.html'
    context_object_name = 'materials'
    paginate_by = 25

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filter_form = MaterialFilterForm(self.request.GET or None)
        material_type = self.request.GET.get('material_type')
        available_materials = queryset
        if material_type in dict(Material.TYPE_CHOICES):
            available_materials = available_materials.filter(material_type=material_type)

        manufacturers = set(
            available_materials
            .order_by()
            .values_list('manufacturer', flat=True)
            .distinct()
        )

        self.filter_form.fields['manufacturer'].choices = [
            ('', 'Всички производители'),
            *[
                (value, label)
                for value, label in Material.MANUFACTURER_CHOICES
                if value in manufacturers
            ]
        ]
        return self.filter_form.filter_queryset(queryset).order_by(
            'material_type',
            'manufacturer',
            'decor_code',
            'thickness',
            'pk',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.order
        context['filter_form'] = self.filter_form


        return context
    

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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        try:
            material_pk = int(self.request.GET.get('material', ''))
        except (TypeError, ValueError):
            raise Http404('Невалиден материал.')

        material = get_object_or_404(Material, pk=material_pk)
        kwargs['material'] = material

        return kwargs

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


class OrderExcelDownloadView(View):
    def get(self, request, order_pk):
        order = get_object_or_404(
            Order,
            pk=order_pk,
            pk__in=request.session.get('order_ids', []),
            status='SUBMITTED',
        )

        if not order.excel_file:
            raise Http404('Няма генериран Excel файл.')

        return FileResponse(
            order.excel_file.open('rb'),
            as_attachment=True,
            filename=f'{order.number}.xlsx',
        )



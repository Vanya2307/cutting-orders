from django.views.generic import FormView, DetailView
from .forms import ClientForm

from .models import Order
from django.shortcuts import redirect

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




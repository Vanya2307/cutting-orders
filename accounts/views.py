from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .forms import RegistrationForm
from .models import Profile

class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)

            Profile.objects.create(
                user=self.object,
                phone=form.cleaned_data['phone'],
                company=form.cleaned_data.get('company', ''),
            )

            clients_group = Group.objects.get(name='Клиенти')
            self.object.groups.add(clients_group)

        login(self.request, self.object)

        return response


class UserLogingView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
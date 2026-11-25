from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .forms import ProfileForm, RegistrationForm
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


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True



class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = ProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    success_message = 'Профилът е обновен.'

    def get_object(self, queryset = None):
        return self.request.user

    def get_initial(self):
        initial = super().get_initial()
        profile = getattr(self.request.user, 'profile', None)

        initial.update({
            'phone': profile.phone.removeprefix('+359') if profile else '',
            'company': profile.company if profile else '',
        })

        return initial

    def form_valid(self, form):
        with transaction.atomic():
            response = super().form_valid(form)

            Profile.objects.update_or_create(
                user=self.object,
                defaults={
                    'phone': form.cleaned_data['phone'],
                    'company': form.cleaned_data['company'],
                },
            )


        return response

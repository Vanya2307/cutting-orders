from django.contrib.auth.views import LogoutView, PasswordChangeView

from django.urls import path, reverse_lazy

from .views import RegistrationView, UserLoginView, UserProfileView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path(
        'password-change/',
        PasswordChangeView.as_view(
            template_name='accounts/password_change.html',
            success_url=reverse_lazy('accounts:profile'),
        ),
        name='password-change',
    ),

]
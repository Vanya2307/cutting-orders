from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

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
    path(
        'password-reset/',
        PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            email_template_name='accounts/password_reset_email.txt',
            subject_template_name='accounts/password_reset_subject.txt',
            success_url=reverse_lazy('accounts:password-reset-done'),
        ),
        name='password-reset',
    ),
    path(
        'password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html',
        ),
        name='password-reset-done',
    ),
    path(
        'reset/<uidb64>/<token>/',

        PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password-reset-complete'),
        ),
        name='password-reset-confirm',

    ),
    path(
        'reset/complete/',
        PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html',
        ),
        name='password-reset-complete',
    ),

]
from django.contrib.auth.views import LogoutView

from django.urls import path

from .views import RegistrationView, UserLogingView

app_name = 'accounts'

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', UserLogingView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
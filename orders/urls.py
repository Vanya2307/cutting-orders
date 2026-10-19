from django.urls import path

from .views import (
    OrderCreateView, 
    OrderDetailView, 
    DetailCreateView, 
    DetailUpdateView, 
    DetailDeleteView,
    OrderDrawingCreateView,
    OrderDrawingDownloadView,
    OrderDrawingDeleteView,
)

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:order_pk>/details/create/', DetailCreateView.as_view(), name='detail-create'),
    path('<int:order_pk>/details/<int:pk>/edit/', DetailUpdateView.as_view(), name='detail-update'),
    path('<int:order_pk>/details/<int:pk>/delete/', DetailDeleteView.as_view(), name='detail-delete'),
    path('<int:order_pk>/drawings/create/', OrderDrawingCreateView.as_view(), name='drawing-create'),
    path('<int:order_pk>/drawings/<int:pk>/download/', OrderDrawingDownloadView.as_view(), name='drawing-download'),
    path('<int:order_pk>/drawings/<int:pk>/delete/', OrderDrawingDeleteView.as_view(), name='drawing-delete'),
]
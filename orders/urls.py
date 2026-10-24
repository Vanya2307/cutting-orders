from django.urls import include, path

from .views import (
    MaterialSelectView,
    OrderCreateView, 
    OrderDetailView, 
    DetailCreateView, 
    DetailUpdateView, 
    DetailDeleteView,
    OrderDrawingCreateView,
    OrderDrawingDownloadView,
    OrderDrawingDeleteView,
    OrderSubmitView,
)

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    path('<int:order_pk>/details/', include([
        path('create/', DetailCreateView.as_view(), name='detail-create'),
        path('<int:pk>/edit/', DetailUpdateView.as_view(), name='detail-update'),
        path('<int:pk>/delete/', DetailDeleteView.as_view(), name='detail-delete'),
    ])),

    path('<int:order_pk>/drawings/', include([
        path('create/', OrderDrawingCreateView.as_view(), name='drawing-create'),
        path('<int:pk>/download/', OrderDrawingDownloadView.as_view(), name='drawing-download'),
        path('<int:pk>/delete/', OrderDrawingDeleteView.as_view(), name='drawing-delete'),
    ])),

    path('<int:order_pk>/materials/', MaterialSelectView.as_view(), name='material-select'),
    path('<int:order_pk>/submit/', OrderSubmitView.as_view(), name='order-submit'),
]
from django.urls import path

from .views import (
    MaterialListView, 
    MaterialDetailView, 
    MaterialCreateView, 
    MaterialUpdateView, 
    MaterialDeleteView, 
    ServiceListView,
    ServiceDetailView,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView,
) 

app_name = "catalog"

urlpatterns = [
    path("materials/", MaterialListView.as_view(), name="material-list"),
    path("materials/<int:pk>/", MaterialDetailView.as_view(), name="material-detail"),
    path("materials/create/", MaterialCreateView.as_view(), name="material-create"),
    path("materials/<int:pk>/edit/", MaterialUpdateView.as_view(), name="material-update"),
    path("materials/<int:pk>/delete/", MaterialDeleteView.as_view(), name="material-delete"),

    path("services/", ServiceListView.as_view(), name="service-list"),
    path("services/create/", ServiceCreateView.as_view(), name="service-create"),
    path("services/<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
    path("services/<int:pk>/edit/", ServiceUpdateView.as_view(), name="service-update"),
    path("services/<int:pk>/delete/", ServiceDeleteView.as_view(), name="service-delete"),
]
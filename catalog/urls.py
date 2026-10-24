from django.urls import include, path

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
    path("materials/", include([
        path("", MaterialListView.as_view(), name="material-list"),
        path("create/", MaterialCreateView.as_view(), name="material-create"),
        path("<int:pk>/", MaterialDetailView.as_view(), name="material-detail"),
        path("<int:pk>/edit/", MaterialUpdateView.as_view(), name="material-update"),
        path("<int:pk>/delete/", MaterialDeleteView.as_view(), name="material-delete"),
    ])),

    path("services/", include([
        path("", ServiceListView.as_view(), name="service-list"),
        path("create/", ServiceCreateView.as_view(), name="service-create"),
        path("<int:pk>/", ServiceDetailView.as_view(), name="service-detail"),
        path("<int:pk>/edit/", ServiceUpdateView.as_view(), name="service-update"),
        path("<int:pk>/delete/", ServiceDeleteView.as_view(), name="service-delete"),
    ])),
]
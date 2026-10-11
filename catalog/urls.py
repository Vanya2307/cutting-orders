from django.urls import path

from .views import MaterialListView, MaterialDetailView, MaterialCreateView, MaterialUpdateView, MaterialDeleteView

app_name = "catalog"

urlpatterns = [
    path("", MaterialListView.as_view(), name="material-list"),
    path("<int:pk>/", MaterialDetailView.as_view(), name="material-detail"),
    path("create/", MaterialCreateView.as_view(), name="material-create"),
    path("<int:pk>/edit/", MaterialUpdateView.as_view(), name="material-update"),
    path("<int:pk>/delete/", MaterialDeleteView.as_view(), name="material-delete"),
]
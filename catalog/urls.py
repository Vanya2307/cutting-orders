from django.urls import path

from .views import MaterialListView, MaterialDetailView, MaterialCreateView

app_name = "catalog"

urlpatterns = [
    path("", MaterialListView.as_view(), name="material-list"),
    path("<int:pk>/", MaterialDetailView.as_view(), name="material-detail"),
    path("create/", MaterialCreateView.as_view(), name="material-create"),
]
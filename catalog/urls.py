from django.urls import path

from .views import MaterialListView, MaterialDetailView

app_name = "catalog"

urlpatterns = [
    path("", MaterialListView.as_view(), name="material-list"),
    path("<int:pk>/", MaterialDetailView.as_view(), name="material-detail")
]
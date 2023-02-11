from django.urls import path
from . import views

app = "kosenai"
urlpatterns = [
    path("contents/", views.GetContents.as_view(), name="contents"),
    path("diagnosis/", views.GetDiagnosis.as_view(), name="diagnosis"),
    path("result/", views.GetResult.as_view(), name="result"),
]

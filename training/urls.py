from django.urls import path
from . import views

app_name = 'training'

urlpatterns = [
    path('', views.TrainingMatrixView.as_view(), name='matrix'),
    path('download/', views.download_matrix, name='download_matrix'),
]

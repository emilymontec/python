from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path('', views.lista_incidentes, name='home'),
    path('create/', views.IncidenteCreateView.as_view(), name='incident_create'),
    path('<int:pk>/', views.IncidenteDetailView.as_view(), name='incident_detail'),
    path('<int:pk>/edit/', views.IncidenteUpdateView.as_view(), name='incident_edit'),
    path('<int:pk>/delete/', views.IncidenteDeleteView.as_view(), name='incident_delete'),
]

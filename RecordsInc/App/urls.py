from django.urls import path
from . import views

app_name = 'App'

urlpatterns = [
    path('', views.lista_incidentes, name='home'),
    path('create/', views.IncidenteCreateView.as_view(), name='incident_create'),
    path('<int:pk>/', views.IncidenteDetailView.as_view(), name='incident_detail'),
    path('<int:pk>/edit/', views.IncidenteUpdateView.as_view(), name='incident_edit'),
    path('<int:pk>/delete/', views.IncidenteDeleteView.as_view(), name='incident_delete'),

    # Projects
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project_edit'),
    path('projects/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('issues/', views.dashboard, name='issue_list'),
    path('export/csv/', views.export_csv, name='export_csv'),
    path('deploy-webhook/', views.deploy_webhook, name='deploy_webhook'),
]
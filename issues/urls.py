from django.urls import path
from . import views

urlpatterns = [
    path('', views.issue_dashboard, name='dashboard'),
    path('issues/', views.issue_dashboard, name='issue_list'),
    path('export/csv/', views.export_issues_csv, name='export_csv'),
]
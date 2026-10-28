from django.urls import path
from . import views

urlpatterns = [
    path('', views.issue_list, name='issue_list'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('issue/<int:pk>/status/', views.update_issue_status, name='update_issue_status'),
    path('report/', views.create_issue, name='create_issue'),
    path('issue/<int:pk>/upvote/', views.upvote_issue, name='upvote_issue'),
]
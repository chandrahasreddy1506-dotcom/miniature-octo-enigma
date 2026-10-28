from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from issues import views as issue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', issue_views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='issues/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='issue_list'), name='logout'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='user_dashboard', permanent=False)),
    path('', include('issues.urls')),
]
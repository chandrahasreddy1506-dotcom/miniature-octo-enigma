from django.contrib import admin
from django.urls import path, include
from issues import views as issue_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('issues.urls')),
    path('accounts/register/', issue_views.register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]
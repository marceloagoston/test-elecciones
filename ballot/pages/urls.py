from django.urls import path

from . import views


urlpatterns = [
    path('', views.DashboardHome.as_view(), name='dashboard_home'),
]

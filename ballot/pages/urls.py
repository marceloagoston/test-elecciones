from django.urls import path

from . import views


urlpatterns = [
    path('', views.Landing.as_view(), name='home'),
    path('dashboard/', views.DashboardHome.as_view(), name='dashboard_home'),
]

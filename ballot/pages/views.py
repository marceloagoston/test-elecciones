from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = 'admin_dashboard.html'
    login_url = 'login'

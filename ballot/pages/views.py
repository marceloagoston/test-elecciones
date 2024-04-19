from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from voting.models import Voter

from accounts.utils import AdminMixin


class Landing(TemplateView):
    template_name = 'front_office/home.html'


class DashboardHome(LoginRequiredMixin, AdminMixin, TemplateView):
    template_name = 'admin_dashboard.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'dashboard'
        context['cant_votantes'] = Voter.objects.all().count()
        context['votos_emitidos'] = Voter.objects.filter(has_voted=True).count()
        return context

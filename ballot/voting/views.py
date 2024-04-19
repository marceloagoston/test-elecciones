from django.shortcuts import redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from django.http import HttpResponseRedirect

from .models import ElectionHandler, PoliticalParty, Voter
from .forms import PoliticalPartyForm, VoterForm


class PoliticalPartyListView(LoginRequiredMixin, ListView):
    model = PoliticalParty
    template_name = 'voting/partidos/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context


class PoliticalPartyCreateView(LoginRequiredMixin, CreateView):
    model = PoliticalParty
    form_class = PoliticalPartyForm
    template_name = 'voting/partidos/form.html'
    success_url = reverse_lazy('political_parties_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'Partido político creado correctamente')
        return super().form_valid(form)


class PoliticalPartyUpdateView(LoginRequiredMixin, UpdateView):
    model = PoliticalParty
    form_class = PoliticalPartyForm
    template_name = 'voting/partidos/form.html'
    success_url = reverse_lazy('political_parties_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'Partido político editado correctamente')
        return super().form_valid(form)


class PoliticalPartyDeleteView(LoginRequiredMixin, DeleteView):
    model = PoliticalParty
    template_name = 'voting/partidos/eliminar.html'
    success_url = reverse_lazy('political_parties_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context


class VoterListView(LoginRequiredMixin, ListView):
    model = Voter
    template_name = 'voting/votantes/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'votantes'
        return context


class VoterCreateView(LoginRequiredMixin, CreateView):
    model = Voter
    form_class = VoterForm
    template_name = 'voting/votantes/form.html'
    success_url = reverse_lazy('voter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'votantes'
        return context

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'Votante creado correctamente')
        return super().form_valid(form)


class VoterUpdateView(LoginRequiredMixin, UpdateView):
    model = Voter
    form_class = VoterForm
    template_name = 'voting/votantes/form.html'
    success_url = reverse_lazy('voter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'votantes'
        return context

    def form_valid(self, form):
        form.save(commit=True)
        messages.success(self.request, 'Votante editado correctamente')
        return super().form_valid(form)


class VoterDeleteView(LoginRequiredMixin, DeleteView):
    model = Voter
    template_name = 'voting/votantes/eliminar.html'
    success_url = reverse_lazy('voter_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'votantes'
        return context

    def post(self, request, pk, *args, **kwargs):
        self.get_object().delete()

        messages.success(request, 'Votante eliminado exitosamente')
        return redirect(self.success_url)


class ElectionHandlerView(LoginRequiredMixin, TemplateView):
    template_name = 'voting/election_handler/handler.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'elecciones'
        context['object'] = ElectionHandler.objects.all().first()
        return context

    def post(self, request, *args, **kwargs):
        obj_instance = self.get_context_data()['object']
        obj_instance.status = obj_instance.next_status
        obj_instance.save()
        return HttpResponseRedirect(self.request.path_info)

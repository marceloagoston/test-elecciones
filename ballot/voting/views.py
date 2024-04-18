from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import PoliticalParty
from .forms import PoliticalPartyForm


class PoliticalPartyListView(LoginRequiredMixin, ListView):
    model = PoliticalParty
    template_name = 'voting/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context


class PoliticalPartyCreateView(LoginRequiredMixin, CreateView):
    model = PoliticalParty
    form_class = PoliticalPartyForm
    template_name = 'voting/form.html'
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
    template_name = 'voting/form.html'
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
    template_name = 'voting/eliminar.html'
    success_url = reverse_lazy('political_parties_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context

import json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from django.http import HttpResponseRedirect

from .models import ElectionHandler, PoliticalParty, Voter, Vote
from .forms import PoliticalPartyForm, VoterForm

from accounts.utils import AdminMixin


class PoliticalPartyListView(LoginRequiredMixin, AdminMixin, ListView):
    model = PoliticalParty
    template_name = 'voting/partidos/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context


class PoliticalPartyCreateView(LoginRequiredMixin, AdminMixin, CreateView):
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


class PoliticalPartyUpdateView(LoginRequiredMixin, AdminMixin, UpdateView):
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


class PoliticalPartyDeleteView(LoginRequiredMixin, AdminMixin, DeleteView):
    model = PoliticalParty
    template_name = 'voting/partidos/eliminar.html'
    success_url = reverse_lazy('political_parties_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'listas'
        return context


class VoterListView(LoginRequiredMixin, AdminMixin, ListView):
    model = Voter
    template_name = 'voting/votantes/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar_active'] = 'votantes'
        return context


class VoterCreateView(LoginRequiredMixin, AdminMixin, CreateView):
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


class VoterUpdateView(LoginRequiredMixin, AdminMixin, UpdateView):
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


class VoterDeleteView(LoginRequiredMixin, AdminMixin, DeleteView):
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


class ElectionHandlerView(LoginRequiredMixin, AdminMixin, TemplateView):
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


class VoteHandlerView(TemplateView):
    template_name = 'voting/front_office/form.html'
    # form_class = FormVotacion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['party_object_list'] = PoliticalParty.objects.all()
        return context

    def post(self, request, *args, **kwargs):

        if ElectionHandler.objects.all().first().status == 'abi':
            with transaction.atomic():
                voter_instance = Voter.objects.get(dni=self.request.POST['dni'])
                voter_instance.has_voted = True
                voter_instance.save()

                voto = None if self.request.POST['lista'] == '0' else self.request.POST['lista']

                Vote.objects.create(political_party_id=voto, district=voter_instance.district)
            messages.success(request, 'Voto emitido correctamente')
        else:
            messages.error(request, 'La elección ya finalizó. No se puede votar')
        return HttpResponseRedirect(reverse_lazy('home'))


@csrf_exempt
def check_puede_votar(request):

    message = 'No puede votar'
    condicion = False

    dni = request.POST.get('dni')

    query = Voter.objects.filter(dni=dni, has_voted=False)
    if query.exists():
        message = 'Puede votar'
        condicion = True

    response_data = json.dumps({'message': message, 'condicion': condicion})
    mimetype = 'application/json'
    return HttpResponse(response_data, mimetype)

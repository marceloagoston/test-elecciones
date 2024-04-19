from django.urls import path

from . import views


urlpatterns = [
    path('', views.PoliticalPartyListView.as_view(), name='political_parties_list'),
    path('crear/', views.PoliticalPartyCreateView.as_view(), name='political_parties_create'),
    path(
        'editar/<int:pk>', views.PoliticalPartyUpdateView.as_view(), name='political_parties_update'
    ),
    path(
        'eliminar/<int:pk>',
        views.PoliticalPartyDeleteView.as_view(),
        name='political_parties_delete',
    ),
    path('votantes/', views.VoterListView.as_view(), name='voter_list'),
    path('votantes/crear/', views.VoterCreateView.as_view(), name='voter_create'),
    path('votantes/editar/<int:pk>', views.VoterUpdateView.as_view(), name='voter_update'),
    path('votantes/eliminar/<int:pk>', views.VoterDeleteView.as_view(), name='voter_delete'),
    path('election-handler/', views.ElectionHandlerView.as_view(), name='election_handler'),
    # Public votation
    path('vote/', views.VoteHandlerView.as_view(), name='vote_election_handler'),
    # AJAX Check puede votar
    path('check-vote/', views.check_puede_votar, name='check_votacion'),
]

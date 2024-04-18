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
]

from .models import ElectionHandler


def custom_context(request):
    election_handler_instance = ElectionHandler.objects.all().first()
    return {
        'election_status': election_handler_instance.status,
    }

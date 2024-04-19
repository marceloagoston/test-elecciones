from datetime import datetime, timedelta

from .models import Voter


def has_voted(dni):
    try:
        voter = Voter.objects.get(dni=dni)
        return voter.has_voted
    except Voter.DoesNotExist:
        return None


def has_voted_percentage():
    total_voters = Voter.objects.count()
    voted_voters = Voter.objects.filter(has_voted=True).count()

    if total_voters == 0:
        return 0

    return (voted_voters / total_voters) * 100


def can_vote(birth_date):
    """Función para validar si una persona es mayor de edad o no

    Params:
        - birth_date: Fecha de nacimiento

    Return
        - Bool: indica si la persona tiene 18 años o mas
    """
    current_date = datetime.now()

    date_avaible = current_date - timedelta(days=365 * 18)

    return birth_date <= date_avaible.date()

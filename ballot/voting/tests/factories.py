from factory import django, Faker, SubFactory

from voting.models import Voter

from districts.tests.factories import DistrictFactory


class VoterFactory(django.DjangoModelFactory):
    class Meta:
        model = Voter

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    dni = Faker('random_int', min=0, max=57000000)
    birth_date = Faker('date_of_birth')
    has_voted = False
    district = SubFactory(DistrictFactory)

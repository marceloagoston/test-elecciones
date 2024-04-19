from factory import django, Faker, SubFactory

from districts.models import District, Province


class ProvinceFactory(django.DjangoModelFactory):
    class Meta:
        model = Province

    name = Faker('state')


class DistrictFactory(django.DjangoModelFactory):
    class Meta:
        model = District

    name = Faker('city')
    province = SubFactory(ProvinceFactory)

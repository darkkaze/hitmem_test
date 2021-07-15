import factory
from apps.missions.models import Hit
from apps.users.tests.factories import HitmenFactory, ManagerFactory
from factory.django import DjangoModelFactory


class HitFactory(DjangoModelFactory):
    class Meta:
        model = Hit

    target = factory.Faker('first_name')
    description = factory.Faker('text')
    managed_by = factory.SubFactory(ManagerFactory)
    hitmen_by = factory.SubFactory(HitmenFactory)

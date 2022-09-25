from django.contrib.auth.models import User
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from core.models import Watchlist

fake = Faker()


class AccountFactory(DjangoModelFactory):
    class Meta(object):
        model = User

    username = LazyAttribute(lambda o: fake.user_name())
    first_name = LazyAttribute(lambda o: fake.first_name())
    last_name = LazyAttribute(lambda o: fake.last_name())
    is_superuser = False
    is_active = True
    is_staff = False


class WatchlistFactory(DjangoModelFactory):
    class Meta(object):
        model = Watchlist

    username_id = SubFactory(AccountFactory)
    name = LazyAttribute(lambda o: fake.name())
    description = LazyAttribute(lambda o: fake.sentence())

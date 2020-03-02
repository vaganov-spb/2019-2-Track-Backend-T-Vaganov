import factory
from faker import Factory
from users.models import User

faker = Factory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = faker.first_name()
    last_name = faker.last_name()
    username = faker.email()
    password = faker.password()

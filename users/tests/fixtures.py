from users.models import User


def create_test_user(name):
    """
    Creates user with 'test' fields.
    'name' argument is identifier added to
    username and email to provide unique constraints.
    """
    return User.objects.create_user(username=f'tester_{name}', email=f'testing_{name}@test.ru', password='qwe123QWE123')

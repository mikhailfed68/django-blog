from users.models import User


def get_test_user_passwd():
    return 'testTestTestDefault'


def create_test_user(name, password=get_test_user_passwd()):
    """
    Creates user with 'test' fields.
    'name' argument is identifier added to
    username and email to provide unique constraints.
    """
    return User.objects.create_user(username=name, email=f'{name}@test.ru', password=password)

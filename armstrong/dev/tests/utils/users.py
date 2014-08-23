import random
try:
    from django.contrib.auth import get_user_model
except ImportError:  # DROP_WITH_DJANGO14
    from django.contrib.auth.models import User
else:
    User = get_user_model()


def generate_random_users(count, **extra_fields):
    """Generator to create ``count`` number of unique random users"""

    num = random.randint(1000, 2000)
    while count > 0:
        fields = dict(
            username="random-user-%d" % num,
            first_name="Some",
            last_name="Random User %d" % num,
            **extra_fields)
        yield User.objects.create(**fields)
        num += random.randint(2, 20)
        count -= 1

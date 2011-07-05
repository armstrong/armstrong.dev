from armstrong.dev.tests.utils.base import ArmstrongTestCase
from django.contrib.auth.models import User
import random

def generate_random_user():
    r = random.randint(10000, 20000)
    return User.objects.create(username="random-user-%d" % r,
            first_name="Some", last_name="Random User %d" % r)


def generate_random_staff_users(n=2):
    orig_users = generate_random_users(n)
    users = User.objects.filter(pk__in=[a.id for a in orig_users])
    users.update(is_staff=True)
    return [a for a in users]


class generate_random_staff_usersTestCase(ArmstrongTestCase):
    def test_returns_2_users_by_default(self):
        self.assertEqual(len(generate_random_staff_users()), 2)

    def test_returns_n_users(self):
        r = random.randint(1, 5)
        self.assertEqual(len(generate_random_staff_users(r)), r)

    def test_all_users_are_staff(self):
        users = generate_random_staff_users()
        for user in users:
            self.assertTrue(user.is_staff)


def generate_random_users(n=2):
    return [generate_random_user() for i in range(n)]
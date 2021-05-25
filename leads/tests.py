from django.contrib import auth
from django.test import TestCase
from .models import User

class AuthTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('test@dom.com', 'test@dom.com', 'pass')
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.save()

    def testLogin(self):
        self.client.login(username='test@dom.com', password='pass')

#Then run the test with python manage.py test <your_app_name>.#AuthTestCase. If this passes, the system is working, maybe look at the #username and password to make sure they are acceptable.

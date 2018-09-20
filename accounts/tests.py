from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status


class SignupTest(TestCase):

    def setUp(self):
        self.details = {
            "username": "ashwani",
            "email": "sonushakya@gmail.com",
            "password": "ashwani1"
        }
        self.header = {
            'HTTP_ACCEPT': 'application/json'
        }

    # TestCase for passing new registration
    def test_signup_pass(self):
        response = self.client.post(
            path='/accounts/register/',
            data=self.details,
            content_type='application/json',
            **self.header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    # TestCase for failing get request
    def test_signup_fail_get(self):
        response = self.client.get(
            path='/accounts/register/',
            content_type='application/json',
            **self.header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

    # TestCase for failing registration by invalid email or password
    def test_signup_fail_post(self):
        details = {
            "username": "ashwani",
            "email": "sonushakya@gmail.com",
            "password": "ashwani"
        }
        response = self.client.post(
            path='/accounts/register/',
            data=details,
            content_type='application/json',
            **self.header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class LogInTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.credentials = {
            "username": "ashwani1",
            'email': 'test@gmail.com',
            'password': 'ashwani1'
        }
        self.header = {
            'HTTP_ACCEPT': 'application/json'
        }
        User.objects.create_user(**self.credentials)

    # TestCase for passing login
    def test_login(self):
        response = self.client.post(
            '/accounts/login/',
            data=self.credentials,
            content_type='application/json',
            **self.header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    # TestCase for failing login
    def test_login_fail(self):
        credentials = {
            "username": "ashwani1",
            'email': 'testfail@gmail.com',
            'password': 'ashwani12'
        }
        response = self.client.post(
            '/accounts/login/',
            data=credentials,
            content_type='application/json',
            **self.header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    # TestCase for failing get request
    def test_login_get(self):
        response = self.client.get(
            '/accounts/login/',
            content_type='application/json',
            **self.header
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )

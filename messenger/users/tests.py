import json
from django.test import TestCase, Client
from users.factories import UserFactory

# Create your tests here.


class FindUser(TestCase):
    def setUp(self):
        self.client = Client()

    def test_find_existing_user(self):
        response = self.client.get('/users/?search=roo')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content, [{"id": 1, "username": "root", "first_name": "", "last_name": ""}])

    def test_find_non_existing_user(self):
        response = self.client.get('/users/?search=psq')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content), 'User not found')

    def test_with_factories(self):
        user = UserFactory()
        response = self.client.get(f'/users/?search={user.username}')
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content[0]['username'], user.username)


class User(TestCase):
    def setUp(self):
        self.client = Client()

    def test_profile_existing(self):
        response = self.client.get('/users/1/')
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)

        obj = {
            'id': content['id'],
            'first name': content['first name'],
            'username': content['username'],
            'date joined': content['date joined'],
        }
        self.assertEqual(obj, {"id": 1, "first name": "", "username": "root", "date joined": "2019-11-06T19:59:29.092Z"})

    def test_profile_non_existing(self):
        response = self.client.get('/users/3/')
        self.assertEqual(response.status_code, 404)

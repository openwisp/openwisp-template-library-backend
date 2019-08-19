import json

from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from mock import Mock, patch
from rest_framework.test import APIClient, APITestCase

from openwisp_users.models import Organization
from openwisp_users.tests.utils import TestOrganizationMixin


class TestAPI(APITestCase, TestOrganizationMixin):

    client = APIClient()

    def setUp(self):
        social_app = SocialApp.objects.create(
            provider='facebook',
            name='Facebook',
            client_id='123123123',
            secret='321321321',
        )

        google_social_app = SocialApp.objects.create(
            provider='google',
            name='Google',
            client_id='11223344',
            secret='55667788',
        )

        site = Site.objects.get_current()
        social_app.sites.add(site)
        google_social_app.sites.add(site)

    @patch('requests.get')
    def test_social_auth(self, mocked_get):
        # fake response for facebook call
        resp_body = {
            "id": "123123123123",
            "first_name": "test",
            "gender": "male",
            "last_name": "user",
            "link": "https://www.facebook.com/test.user",
            "locale": "en_US",
            "name": "test user",
            "timezone": 2,
            "updated_time": "2014-08-13T10:14:38+0000",
            "username": "test.user",
            "verified": True
        }
        response = Mock()
        response.status_code = 200
        response.json.return_value = resp_body
        mocked_get.return_value = response
        users_count = get_user_model().objects.all().count()
        payload = {
            'access_token': 'abc123'
        }

        response = self.client.post(reverse('fb_login'), data=payload, status_code=200)
        self.assertIn('key', str(response.content))
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

        # make sure that second request will not create a new user
        response = self.client.post(reverse('fb_login'), data=payload, status_code=200)
        self.assertIn('key', str(response.content))
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

    @patch('requests.get')
    def _twitter_social_auth(self, mocked_get):
        # fake response for google call
        resp_body = {
            "id": "123123123123",
        }

        response = Mock()
        response.status_code = 200
        response.json.return_value = resp_body
        mocked_get.return_value = response

        users_count = get_user_model().objects.all().count()
        payload = {
            'access_token': 'abc123',
            'token_secret': '1111222233334444'
        }

        self.client.post(reverse('google_login'), data=payload)

        self.assertIn('key', str(response.content))
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

        # make sure that second request will not create a new user
        self.client.post(reverse('google_login'), data=payload, status_code=200)
        self.assertIn('key', str(response.content))
        self.assertEqual(get_user_model().objects.all().count(), users_count + 1)

    @patch('allauth.account.views.ConfirmEmailView.post')
    def test_signup_redirect(self, mocked_post):
        mocked_post.return_value = None
        key = 'Mw:1hltk5:gwIwN2aQWMbmi3fnUD8e4qGI_5c'
        path = reverse('confirm_email', args=[key])
        response = self.client.post(path)
        mocked_post.assert_called_once()
        self.assertEqual(response.status_code, 302)

    def test_api_list_org(self):
        user = self._create_admin()
        org1 = self._create_org(name='org1', slug='org1')
        org1.add_user(user)
        path = reverse('list_orgs')
        self.client.force_login(user)
        response = self.client.get(path)
        self.assertContains(response, 'org1')

    def test_api_detail_org(self):
        user = self._create_admin()
        org1 = self._create_org(name='org1', slug='org1')
        org1.add_user(user)
        path = reverse('org_detail', args=[org1.pk])
        self.client.force_login(user)
        response = self.client.get(path)
        self.assertContains(response, 'org1')

    def test_api_create_org(self):
        user = self._create_admin()
        data = {
            'description': 'some description',
            'name': 'org1',
            'email': 'org1@gmail.com',
            'url': 'http://org1.com',
            'slug': 'org1'
        }
        path = reverse('list_orgs')
        self.client.force_login(user)
        response = self.client.post(path, data=data)
        queryset = Organization.objects.filter(name='org1')
        self.assertEqual(queryset.count(), 1)
        self.assertEqual(response.status_code, 200)
        # test create an org which already exist
        response = self.client.post(path, data=data)
        self.assertContains(response, 'org_errors', status_code=400)

    def test_api_edit_org(self):
        user = self._create_admin()
        org = self._create_org(name='org1', slug='org1')
        org.add_user(user)
        path = reverse('org_detail', args=[org.pk])
        self.client.force_login(user)
        self.client.put(path, data=json.dumps({'slug': 'org11', 'name': 'org11'}),
                        content_type='application/json')
        queryset = Organization.objects.filter(slug='org11')
        self.assertEqual(queryset.count(), 1)
        self.client.delete(path)
        queryset = Organization.objects.filter(name='org2')
        self.assertEqual(queryset.count(), 0)

from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from mock import Mock, patch
from rest_framework.test import APIClient, APITestCase


class TestAPI(APITestCase):
    """
    Helper base class for API test
    """
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

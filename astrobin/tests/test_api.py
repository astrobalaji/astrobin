# Django
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

# AstroBin
from astrobin.models import App, AppApiKeyRequest


class APITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'test', 'test@test.com', 'password')

    def tearDown(self):
        self.user.delete()

    ###########################################################################
    # API KEY REQUESTS                                                        #
    ###########################################################################

    def test_app_api_key_request_view(self):
        # Login required
        response = self.client.get(reverse('app_api_key_request'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=' + reverse('app_api_key_request'),
            status_code = 302,
            target_status_code = 200)

        self.client.login(username = 'test', password = 'password')
        response = self.client.get(reverse('app_api_key_request'))
        self.assertEquals(response.status_code, 200)
        self.assertEquals('form' in response.context[0], True)

        response = self.client.post(reverse('app_api_key_request'), {
            'name': 'Test',
            'description': 'Description'
        }, follow = True)
        self.assertEquals(response.status_code, 200)
        requests = AppApiKeyRequest.objects.filter(
            name = 'Test', description = 'Description')
        self.assertEquals(requests.count(), 1)
        requests.delete()
        self.client.logout()

    def test_app_api_keys_list_view(self):
        # Login required
        response = self.client.get(reverse('app_api_key_request'))
        self.assertRedirects(
            response,
            '/accounts/login/?next=' + reverse('app_api_key_request'),
            status_code = 302,
            target_status_code = 200)

        # Make a request
        self.client.login(username = 'test', password = 'password')
        response = self.client.post(reverse('app_api_key_request'), {
            'name': 'Test',
            'description': 'Description'
        }, follow = True)
        self.assertEquals(response.status_code, 200)

        request = AppApiKeyRequest.objects.all()[0]
        request.approve()
        app = App.objects.all()[0]

        # Get the list page
        response = self.client.get(reverse('user_page_api_keys', args = (self.user.username,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, app.key)

        request.delete()
        app.delete()
        self.client.logout()

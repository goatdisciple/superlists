from unittest.mock import patch
from django.contrib.auth import get_user_model
from django.test import TestCase
User = get_user_model()

from accounts.authentication import (
    PERSONA_VERIFY_URL, DOMAIN, PersonaAuthenticationBackend
)


@patch('accounts.authentication.requests.post')
class AuthenticateTest(TestCase):

    def setUp(self):
        self.backend = PersonaAuthenticationBackend()
        user = User(email='other@user.com')
        user.save()


    def test_sends_assertion_to_mozilla_with_domain(self, mock_post):
        self.backend.authenticate('an assertion')
        mock_post.assert_called_once_with(
            PERSONA_VERIFY_URL,
            data = {'assertion': 'an assertion', 'audience': DOMAIN}
        )

    def test_returns_none_if_response_errors(self, mock_post):
        mock_post.return_value.ok = False
        mock_post.return_value.json.return_value = {}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_returns_none_if_status_not_okay(self, mock_post):
        mock_post.return_value.json.return_value = {'status': 'not okay!'}
        user = self.backend.authenticate('an assertion')
        self.assertIsNone(user)

    def test_finds_existing_user_with_email(self, mock_post):
        existing_user = User.objects.create(email='a@b.com')
        mock_post.return_value.json.return_value = {
            'status': 'okay', 'email': 'a@b.com'
        }
        returned_user = self.backend.authenticate('an assertion')
        self.assertEqual(existing_user, returned_user)
        
    def test_creates_new_user_if_necessary_for_valid_assertion(self, mock_post):
        mock_post.return_value.json.return_value = {
            'status': 'okay', 'email': 'new@user.com'
        }
        returned_user = self.backend.authenticate('an assertion')
        self.assertEqual(User.objects.count(), 2)
        self.assertNotEqual(returned_user, User.objects.get(email='other@user.com'))
        self.assertEqual(returned_user, User.objects.get(email='new@user.com'))


class GetUserTest(TestCase):

    def test_gets_user_by_email(self):
        backend = PersonaAuthenticationBackend()
        other_user = User(email='other@user.com')
        other_user.username = 'otheruser'
        other_user.save()
        desired_user = User.objects.create(email='a@b.com')
        found_user = backend.get_user('a@b.com')
        self.assertEqual(found_user, desired_user)

    def test_returns_none_if_no_user_with_that_email(self):
        backend = PersonaAuthenticationBackend()
        self.assertIsNone(backend.get_user('a@b.com'))

    def test_is_authenticated(self):
        user = User()
        self.assertTrue(user.is_authenticated())

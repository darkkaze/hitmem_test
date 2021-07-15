from django.test import TestCase
from django.urls import reverse

from .factories import BigBossFactory, HitmenFactory, ManagerFactory


class AuthRequiredHitmenViewsTestCase(TestCase):

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.hitmen = HitmenFactory()

    def test_hitmen_list_permission_denied(self):
        resp = self.client.get(reverse('hitmen_list'))
        self.assertEqual(resp.status_code, 403)

    def test_hitmen_create_permission_denied(self):
        resp = self.client.get(reverse('hitmen_create'))
        self.assertEqual(resp.status_code, 403)

    def test_hitmen_details_permission_denied(self):
        resp = self.client.get(
            reverse('hitmen_detail', kwargs={'pk': self.hitmen.id}))
        self.assertEqual(resp.status_code, 403)


class HitmenViewsAuthTestCase(TestCase):

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.hitmen = HitmenFactory()
        self.client.force_login(self.hitmen)

    def test_hitmen_list_permission_denied(self):
        resp = self.client.get(reverse('hitmen_list'))
        self.assertEqual(resp.status_code, 403)

    def test_hitmen_create_permission_denied(self):
        resp = self.client.get(reverse('hitmen_create'))
        self.assertEqual(resp.status_code, 403)

    def test_hitmen_details_permission_denied(self):
        resp = self.client.get(
            reverse('hitmen_detail', kwargs={'pk': self.hitmen.id}))
        self.assertEqual(resp.status_code, 403)


class ManagerViewsAuthTestCase(TestCase):

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.manager = ManagerFactory()
        self.hitmen = ManagerFactory(managed_by=self.manager)
        self.client.force_login(self.manager)

    def test_hitmen_list_ok(self):
        resp = self.client.get(reverse('hitmen_list'))
        self.assertEqual(resp.status_code, 200)

    def test_hitmen_create_ok(self):
        resp = self.client.get(reverse('hitmen_create'))
        self.assertEqual(resp.status_code, 200)

    def test_hitmen_details_ok(self):
        resp = self.client.get(
            reverse('hitmen_detail', kwargs={'pk': self.hitmen.id}))
        self.assertEqual(resp.status_code, 200)

    def test_hitmen_create_post_email_error(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "first_name": "John",
                "last_name": "Do",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbw"})
        self.assertFormError(resp, 'form', 'email', 'This field is required.')

    def test_hitmen_create_post_email_format_error(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "invalid_format",
                "first_name": "John",
                "last_name": "Do",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbw"})
        self.assertFormError(resp, 'form', 'email', 'Enter a valid email address.')

    def test_hitmen_create_post_first_name_error(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "John@hitmens.com",
                "last_name": "Do",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbw"})                
        self.assertFormError(resp, 'form', 'first_name', 'This field is required.')

    def test_hitmen_create_post_last_name_error(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "John@hitmens.com",
                "first_name": "John",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbw"})
        self.assertFormError(resp, 'form', 'last_name', 'This field is required.')

    def test_hitmen_create_password_error(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "John@hitmens.com",
                "first_name": "John",
                "last_name": "Do"})                
        self.assertFormError(resp, 'form', 'password1', 'This field is required.')

    def test_hitmen_create_password_match_error(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "John@hitmens.com",
                "first_name": "John",
                "last_name": "Do",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbwcc"})
        self.assertFormError(resp, 'form', 'password2', "Passwords don't match")

    def test_hitmen_create_post_ok(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "John@hitmens.com",
                "first_name": "John",
                "last_name": "Do",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbw"})                
        self.assertRedirects(resp, reverse('hitmen_list'))


class BigBossViewsAuthTestCase(TestCase):
    """
    notes:
        I consider it not worth repeating all the tests of the form
    """

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.bigboss = BigBossFactory()
        self.manager = ManagerFactory()
        self.hitmen = ManagerFactory(managed_by=self.bigboss)
        self.client.force_login(self.bigboss)

    def test_hitmen_list_ok(self):
        resp = self.client.get(reverse('hitmen_list'))
        self.assertEqual(resp.status_code, 200)

    def test_hitmen_create_ok(self):
        resp = self.client.get(reverse('hitmen_create'))
        self.assertEqual(resp.status_code, 200)

    def test_hitmen_details_ok(self):
        resp = self.client.get(
            reverse('hitmen_detail', kwargs={'pk': self.hitmen.id}))
        self.assertEqual(resp.status_code, 200)

    def test_hitmen_create_post_ok(self):
        resp = self.client.post(
            reverse('hitmen_create'),
            {
                "email": "John@hitmens.com",
                "first_name": "John",
                "last_name": "Do",
                "password1": "y4v4J3cWbw",
                "password2": "y4v4J3cWbw",
                "managed_by": self.manager.id})                
        self.assertRedirects(resp, reverse('hitmen_list'))

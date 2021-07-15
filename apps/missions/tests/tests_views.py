from apps.missions.models import Hit
from apps.users.tests.factories import HitmenFactory
from django.test import TestCase
from django.urls import reverse

from .factories import HitFactory


class AuthRequiredHitViewsTestCase(TestCase):

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.hit = HitFactory()

    def test_hitmen_list_permission_denied(self):
        resp = self.client.get(reverse('hit_list'))
        self.assertEqual(resp.status_code, 403)

    def test_hitmen_create_permission_denied(self):
        resp = self.client.get(reverse('hit_create'))
        self.assertEqual(resp.status_code, 403)

    def test_hitmen_details_permission_denied(self):
        resp = self.client.get(
            reverse('hit_detail', kwargs={'pk': self.hit.id}))
        self.assertEqual(resp.status_code, 403)


class HitViewsWrongHitmenTestCase(TestCase):
    """
    check hitmen can't create
    and can't see hit form other hitmens
    """

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.hit = HitFactory()
        self.hitmen = HitmenFactory()
        self.client.force_login(self.hitmen)

    def test_hit_create_permission_denied(self):
        resp = self.client.get(reverse('hit_create'))
        self.assertEqual(resp.status_code, 403)

    def test_hit_details_permission_denied(self):
        resp = self.client.get(
            reverse('hit_detail', kwargs={'pk': self.hit.id}))
        self.assertEqual(resp.status_code, 403)


class HitViewsHitmensTestCase(TestCase):
    """
    create two hitmens, check if each hitmen see the correct content
    """

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.hit1 = HitFactory()
        self.hitmen1 = self.hit1.hitmen_by
        self.hit2 = HitFactory()
        self.hitmen2 = self.hit2.hitmen_by

    def test_hitmen1_see_correct_content(self):
        self.client.force_login(self.hitmen1)
        resp = self.client.get(reverse('hit_list'))
        self.assertContains(resp, self.hit1.target)
        self.assertNotContains(resp, self.hit2.target)

    def test_hitmen2_see_correct_content(self):
        self.client.force_login(self.hitmen2)
        resp = self.client.get(reverse('hit_list'))
        self.assertContains(resp, self.hit2.target)
        self.assertNotContains(resp, self.hit1.target)


class HitViewsUpdateTestCase(TestCase):
    """
    hitmen can see details and update status
    manager can edit the details
    """

    def setUp(self):
        """
        Setup run before every test method.
        """
        self.hit = HitFactory()
        self.hitmen = self.hit.hitmen_by
        self.manager = self.hit.managed_by

    def test_hitmen_update(self):
        self.client.force_login(self.hitmen)
        resp = self.client.post(
            reverse('hit_detail', kwargs={"pk": self.hit.id}),
            {
                "status": "completed"})                
        self.assertRedirects(resp, reverse('hit_list'))

    def test_hitmen_see_details(self):
        self.client.force_login(self.hitmen)
        resp = self.client.get(
            reverse('hit_detail', kwargs={"pk": self.hit.id}))                
        self.assertContains(resp, "target")

    def test_hitmen_cant_update(self):
        self.client.force_login(self.hitmen)
        resp = self.client.post(
            reverse('hit_detail', kwargs={"pk": self.hit.id}),
            {
                "target": "new name"})                
        hit = Hit.objects.get(id=self.hit.id)
        self.assertNotEqual(hit.target, "new name")

    def test_manager_can_update(self):
        self.client.force_login(self.manager)
        resp = self.client.post(
            reverse('hit_detail', kwargs={"pk": self.hit.id}),
            {
                "target": "new name",
                "description": self.hit.description,
                "hitmen_by": self.hit.hitmen_by.id})                
        hit = Hit.objects.get(id=self.hit.id)
        self.assertEqual(hit.target, "new name")

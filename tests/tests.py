from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.urls import reverse
from tests.admin import ModelCentralAdmin
from tests import models


class AdminStatusTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.central = models.ModelCentral.objects.create(
            name='Central Model'
        )

    def admin_login(self):
        u = User.objects.create_superuser('testuser', password='secret')

        c = Client()
        c.force_login(u)
        return c

    def test_sidebar(self):
        client = AdminStatusTest.admin_login(self)
        change_url = reverse('admin:tests_modelcentral_change', args=(self.central.id,))
        response = client.get(change_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h2>Related Objects</h2>')


class RelatedFieldsTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.central = models.ModelCentral.objects.create(
            name='Central Model'
        )
        self.model_admin = ModelCentralAdmin(models.ModelCentral, self.site)

    def test_fk(self):
        foreign = models.ModelA.objects.create(
            name='Foreign Key Test'
        )
        self.central.foreign_key_a = foreign
        self.central.save()

        related_sidebar = self.model_admin.related_fields(self.central.id)
        self.assertEqual(related_sidebar[0]['header'], 'Foreign Key A')

    def test_reverse_fk(self):
        models.ModelFK.objects.create(
            name='Foreign Key Test',
            foreign_key_c=self.central
        )

        related_sidebar = self.model_admin.related_fields(self.central.id)
        self.assertEqual(related_sidebar[0]['header'], 'Model Fk')

    def test_m2m(self):
        m2m_list = [models.ModelB.objects.create(name=f'M2M Test {x}') for x in range(1, 4)]
        self.central.m2m_b.set(m2m_list)
        self.central.save()

        related_sidebar = self.model_admin.related_fields(self.central.id)
        self.assertEqual(related_sidebar[0]['header'], 'M2M B')
        self.assertEqual(len(related_sidebar[0]['fields']), 3)

    def test_reverse_m2m(self):
        for x in range(1, 4):
            m = models.ModelMM.objects.create(name=f'M2M Test {x}')
            m.m2m_c.set([self.central])

        related_sidebar = self.model_admin.related_fields(self.central.id)
        self.assertEqual(related_sidebar[0]['header'], 'Modelmm')
        self.assertEqual(len(related_sidebar[0]['fields']), 3)

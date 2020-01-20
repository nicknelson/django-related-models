from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.test import TestCase, Client
from django.urls import reverse
from tests.admin import ModelCentralAdmin
from tests import models


class AdminStatusTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def admin_login(self):
        u, created = User.objects.get_or_create(username='testuser', password='secret')

        c = Client()
        c.force_login(u)
        return c

    def test_admin_status(self):
        pass

    def test_sidebar(self):
        pass
        # test returning related fields
        # client = AdminStatusTest.admin_login(self)
        # change_url = reverse('admin:tests_modelcentral_change', args=(central.id,))
        # client.get(change_url)


class ForeignKeyRelationshipTest(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_foreign_key(self):
        # create model relationships
        foreign = models.ModelA.objects.create(
            name='Foreign Key Test'
        )
        central = models.ModelCentral.objects.create(
            name='Central Model',
            foreign_key_a=foreign
        )

        model_admin = ModelCentralAdmin(models.ModelCentral, self.site)
        # print(model_admin)
        related_sidebar = model_admin.related_fields(central.id)
        print(related_sidebar)
        self.assertIs(True, True)

# -*- coding: utf-8 -*-
from fakturahr.tests.base import BaseTestCase


class ClientTestCas(BaseTestCase):
    def test_client_list(self):
        client = self.add_client()
        response = self.app.get('/client/list')
        assert response.status_code == 200

    def test_client_new(self):
        from fakturahr.models.models import Client
        response = self.app.post('/client/new',
                                 data={
                                     'name': u'MyClient',
                                     'address': u'Client Address 123',
                                     'city': u'Town'
                                 })
        client = self.session.query(Client).filter(Client.name == u'MyClient', Client.deleted == False).first()
        assert client is not None

    def test_client_new_error(self):
        from fakturahr.models.models import Client
        response = self.app.post('/client/new',
                                 data={
                                     'address': u'Client Address 123',
                                     'city': u'Town'
                                 })
        client = self.session.query(Client).filter(Client.name == u'MyClient', Client.deleted == False).first()
        assert client is None



# -*- coding: utf-8 -*-

from django.test import RequestFactory, TestCase

from attachments.utils import session, url_filename

from .models import Document

import io


class AttachmentTests (TestCase):

    def test_url_filename(self):
        self.assertEqual(url_filename(u'Résumé.pdf'), 'R%C3%A9sum%C3%A9.pdf')

    def test_json_field(self):
        d = {
            'key': 'value',
            'number': 42,
        }
        Document.objects.create(data=d)
        doc = Document.objects.get()
        self.assertEqual(doc.data, d)

    def test_upload(self):
        att_data = b'some data'
        request = RequestFactory().get('/test/page/')
        sess = session(request)
        att = io.BytesIO(att_data)
        att.name = 'testfile'
        response = self.client.post('/attachments/%s/' % sess.uuid, {'attachment': att})
        self.assertEqual(response.json(), {
            'ok': True,
            'file_name': att.name,
            'file_size': len(att_data),
        })
        upload = sess.uploads.get()
        self.assertEqual(upload.file_name, att.name)
        self.assertEqual(upload.file_size, len(att_data))

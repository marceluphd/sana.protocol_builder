from django.test import TestCase
from django.contrib.auth.models import User
from editor.models import Procedure

class ProcedureTest(TestCase):
    def setUp(self):
        test_user = User.objects.create_user('TestUser', 'test@sanaprotocolbuilder.me', 'testpassword')
        test_user.save()

        Procedure.objects.create(author='tester', title='test procedure', owner=test_user)

    def test_procedures_are_initialized(self):
        proc = Procedure.objects.get(author='tester')
        self.assertEquals(proc.author, 'tester')
        self.assertEquals(proc.title, 'test procedure')
        self.assertEquals(proc.version, '')

    def test_str(self):
        proc = Procedure.objects.get(author='tester')
        expected = '<Procedure title="test procedure" author="tester" version="">\n</Procedure>'
        self.assertEquals(str(proc), expected)
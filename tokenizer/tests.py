from django.test import TestCase

from models import Tokenizer, Token
from users.models import User

class TokenizerTestCase(TestCase):

    def test_tokenizer_assigns_token(self):
        usr = User.create('Test123', 'Test', 'Test')
        tok = Tokenizer.assignToken(usr)
        self.assertEquals(usr.token_set.all()[0], tok)

    def test_tokenizer_authenticates(self):
        user_id = 'Test123'
        password = 'Test'
        usr = User.create(user_id, password, 'Test')
        usr.save()
        tok = Tokenizer.assignToken(usr)
        self.assertTrue(Tokenizer.authenticate(user_id,tok.value))


class TokenTestCase(TestCase):

    def test_token_creates_successfully(self):
        token = Token()
        self.assertEqual(type(token), Token)
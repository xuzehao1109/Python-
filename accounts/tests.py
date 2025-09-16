from django.test import TestCase

from . import totp


class TOTPHelpersTests(TestCase):
    def test_totp_roundtrip(self):
        secret = totp.random_base32_secret()
        token = totp.totp_token(secret, timestamp=0)
        self.assertTrue(totp.verify_totp(secret, token, window=0, interval=30, digits=6))

    def test_totp_rejects_invalid(self):
        secret = totp.random_base32_secret()
        self.assertFalse(totp.verify_totp(secret, 'abcdef'))
        self.assertFalse(totp.verify_totp(secret, ''))

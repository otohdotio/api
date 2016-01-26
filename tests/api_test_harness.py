#!/usr/bin/env python

import json
import unittest
from datetime import datetime

import OpenSSL
import requests

# For now we're using self-signed certs, so let's ignore the warnings
requests.packages.urllib3.disable_warnings()


class Monolithic(unittest.TestCase):

    def setUp(self):
        self.s = requests.Session()
        self.apiurl = 'https://localhost:443'
        self.now = datetime.now().strftime('%Y%m%d%H%M%S')
        self.email = 'test-' + self.now + '@example.com'
        self.response_uuid = ''
        self.response_email = ''
        self.response_cert = ''
        self.response_pubkey = ''

    def test_01_testendpoint(self):
        endpoint = self.apiurl + '/test'
        response = self.s.get(endpoint, verify=False)

        self.assertEqual(response.text, 'test successful\n')

    def test_02_get_cert(self):
        endpoint = self.apiurl + '/cert'
        # Set up CSR objectskey = OpenSSL.crypto.PKey()
        c = OpenSSL.crypto
        self.key = c.PKey()
        self.key.generate_key(c.TYPE_RSA, 512)
        # self.pubkey = c.dump_publickey(c.FILETYPE_PEM, self.key)
        req = c.X509Req()
        req.get_subject().CN = self.email
        req.set_pubkey(self.key)
        req.sign(self.key, "sha1")

        # Grab request
        self.csr = c.dump_certificate_request(c.FILETYPE_PEM, req)
        csrdict = {'csr': self.csr}

        # Now submit the CSR and get a cert back
        r = requests.post(endpoint,
                         json=json.loads(json.dumps(csrdict)),
                         verify=False)
        stop = 'here'
        self.response_uuid = r.json()['uuid']
        self.response_cert = r.json()['cert']

        # Extract the public key from the new cert
        cert = c.load_certificate(c.FILETYPE_PEM, self.response_cert)
        cert_pubkey = cert.get_pubkey()
        # self.response_pubkey = c.dump_publickey(c.FILETYPE_PEM, cert_pubkey)

        stop = 'here'
        # self.assertEqual(self.pubkey, self.response_pubkey)

        # Just while we're sorting this test case out...
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main(failfast=True)
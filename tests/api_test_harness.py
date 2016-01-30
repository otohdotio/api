#!/usr/bin/env python

import json
import unittest
from datetime import datetime

import OpenSSL
import requests

# For now we're using self-signed certs, so let's ignore the warnings
requests.packages.urllib3.disable_warnings()


class Monolithic(unittest.TestCase):
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    response_uuid = ''
    response_cert = ''
    response_x509 = OpenSSL.crypto.X509

    def setUp(self):
        self.s = requests.Session()
        self.apiurl = 'https://localhost:443'
        self.email = 'test-' + self.__class__.now + '@example.com'
        self.response_uuid = ''
        self.response_cert = ''
        self.response_x509 = OpenSSL.crypto.X509

    def test_01_testendpoint(self):
        endpoint = self.apiurl + '/test'
        response = self.s.get(endpoint, verify=False)

        self.assertEqual(response.text, 'test successful\n')

    def test_02_submit_csr_get_cert(self):
        endpoint = self.apiurl + '/csr'
        # Set up CSR objectskey = OpenSSL.crypto.PKey()
        c = OpenSSL.crypto
        self.key = c.PKey()
        self.key.generate_key(c.TYPE_RSA, 512)
        req = c.X509Req()
        req.get_subject().CN = self.email
        req.set_pubkey(self.key)
        req.sign(self.key, "sha256")

        # Grab request
        self.csr = c.dump_certificate_request(c.FILETYPE_PEM, req)
        csrdict = {'csr': self.csr, 'key_use': 'ke'}
        # Now submit the CSR and get a cert back, then save them for later use
        r = requests.post(endpoint,
                          json=json.loads(json.dumps(csrdict)),
                          verify=False)
        self.__class__.response_uuid = r.json()['uuid']
        self.__class__.response_cert = r.json()['cert']

        # Extract the public key and email address from the new cert
        cert = c.load_certificate(c.FILETYPE_PEM, self.__class__.response_cert.replace('\\n', '\n'))
        cert_subject = cert.get_subject()
        cert_cn = cert_subject.commonName

        # Save off the X509 object for use in later test cases
        self.__class__.response_x509 = cert

        # Verify that we got back an X.509 certificate
        self.assertTrue(isinstance(cert, OpenSSL.crypto.X509))

        # Verify that the certificate's email address matches what we sent
        self.assertEqual(self.email, cert_cn)
        # Unfortuneatly, the dump_publickey branch hasn't been merged into
        # the production pyOpenSSL module. So these next lines won't work.
        # TODO: try and get this PR accepted by the upstream community
        # self.response_pubkey = c.dump_publickey(c.FILETYPE_PEM, cert_pubkey)
        # self.pubkey = c.dump_publickey(c.FILETYPE_PEM, self.key)

    def test_03_get_cert_by_uuid(self):
        endpoint = self.apiurl + '/cert'
        payload = {'uuid': self.__class__.response_uuid}
        rc = self.__class__.response_cert
        r = requests.get(endpoint,
                         params=payload,
                         verify=False)
        got_cert = r.json()['cert']

        # Doing this because assertEqual doesn't like the length of the cert
        # strings.
        passed = False
        if rc == got_cert:
            passed = True
        self.assertTrue(passed)

    def test_04_get_cert_by_cn(self):
        endpoint = self.apiurl + '/cert'
        payload = {'cn': self.email}
        rc = self.__class__.response_cert
        r = requests.get(endpoint,
                         params=payload,
                         verify=False)
        got_cert = r.json()['cert']

        # Doing this because assertEqual doesn't like the length of the cert
        # strings.
        passed = False
        if rc == got_cert:
            passed = True
        self.assertTrue(passed)


if __name__ == '__main__':
    unittest.main(failfast=True)
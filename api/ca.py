import OpenSSL
import yaml


class CA(object):

    def __init__(self, **kwargs):
        self.config_file = kwargs['config']
        try:
            config_handle = open(self.config_file)
            config_string = config_handle.read()
            self.config_dict = yaml.load(config_string)
        except Exception as e:
            raise Exception('could not parse yaml config file: ' +
                            self.config_file + ':' + str(e))

    def create_cert(self, csr, key_use, sn, ca_bool):
        # We default usage to signing
        long_use = 'nonRepudiation, digitalSignature'

        # Grab signing cert from config file
        ca_cert = self.config_dict['signing_cert']
        ca_key = self.config_dict['signing_key']
        ### Left off here -- I think I removed the key password, which
        # probably won't work with pyOpenSSL. Need to regenerate the cert
        ca_key_passwd = self.config_dict['signing_key_passwd']

        # Currently only support key encipherment and signing certs
        if key_use != 'ke' and key_use != 'ds':
            raise Exception('create_cert failed: invalid key_use:' +
                            ' valid arguments are ds or ke')
        else:
            if key_use == 'ke':
                long_use = 'keyEncipherment'

        # Crate cert objects for our signing certs
        ca_cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                                  ca_cert)
        ca_key = OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM,
                                                ca_key, ca_key_passwd)

        # Create the CSR object
        req = OpenSSL.crypto.load_certificate_request(OpenSSL.crypto.FILETYPE_PEM,
                                                      csr)

        # Now we get down to business
        ca_flag = 'CA:FALSE'
        if ca_bool is True:
            ca_flag = 'CA:TRUE'
        cert = OpenSSL.crypto.X509()
        cert.set_version(3)
        cert.add_extensions([OpenSSL.crypto.X509Extension("basicConstraints",
                                                          True,
                                                          ca_flag),
                             OpenSSL.crypto.X509Extension('keyUsage',
                                                          True,
                                                          long_use)])
        cert.set_subject(req.get_subject())
        cert.set_serial_number(sn)
        cert.gmtime_adj_notBefore(0)
        # TODO: 10 year certs for now, make this configurable
        cert.gmtime_adj_notAfter(24 * 60 * 60 * 356 * 10)
        cert.set_issuer(ca_cert.get_subject())
        cert.set_pubkey(req.get_pubkey())
        cert.sign(ca_key, "sha256")

        # Now return the plain text (PEM) of the new cert
        return OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_PEM,
                                               cert)

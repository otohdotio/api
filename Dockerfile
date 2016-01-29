FROM centos:latest

MAINTAINER "Jason Callaway" <jason@jasoncallaway.com>

# Install RPMs first
RUN yum update -y && \
    yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    yum install -y httpd mod_ssl mod_wsgi && \
    yum install -y libffi-devel openssl-devel && \
    yum install -y gcc python-devel python-pip && \
    yum install -y MySQL-python
# In production we'll want to yum clean all, but we'll leave the cache around
# now for build speed
#    yum clean all

# Now install all our Python modules
RUN pip install cherrypy && \
    pip install cassandra-driver && \
    pip install PyYAML && \
    pip install pyOpenSSL && \
    pip install uuid

# Set up CA and httpd configs
### For now, copy from a local clone (better for planes)
#RUN git clone --branch prod git@github.com:otohdotio/api.git /api
ADD ssl/ssl.conf /etc/httpd/conf.d/ssl.conf
ADD ssl/server.crt /etc/pki/tls/certs/server.crt
ADD ssl/server.key /etc/pki/tls/private/server.key
ADD ssl/server-ca.crt /etc/pki/tls/certs/server-ca.crt
ADD ca_config.yaml /ca_config.yaml
RUN mkdir -p /var/www/html/api && \
    mkdir -p /var/log/httpd
ADD api/*.py /var/www/html/api/
RUN chmod +x /var/www/html/api/*.py

# Suppress httpd FQDN error
RUN echo "ServerName api.otoh.io" >> /etc/httpd/conf/httpd.conf

# Fix ownerships
RUN chown -R apache:apache /var/log/httpd && \
    chmod -R 660 /etc/pki/tls/certs/server.* && \
    chmod -R 660 /etc/pki/tls/private/server.key && \
    chown -R apache:apache /var/www/html && \
    echo "export PYTHONPATH=/var/www/html/api:${PYTHONPATH}" >> /root/.bashrc

# Fix the main httpd.conf Log directives
RUN sed -i -e 's/^ErrorLog.*/ErrorLog \/proc\/self\/fd\/1/' /etc/httpd/conf/httpd.conf && \
    sed -i -e 's/CustomLog "logs\/access_log" combined/CustomLog \/proc\/self\/fd\/1 combined/' /etc/httpd/conf/httpd.conf

# We shouldn't have more than one API container running per host, so we'll go
# ahead and bind to the host's 443
EXPOSE 443

# Finally, fire up httpd
CMD ["-D", "FOREGROUND"]
ENTRYPOINT ["/usr/sbin/httpd"]

#END

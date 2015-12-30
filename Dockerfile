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
ADD ssl/host.crt /etc/pki/tls/certs/host.crt
ADD ssl/host.key /etc/pki/tls/private/host.key
ADD ssl/ca.crt /etc/pki/tls/certs/ca.crt
RUN mkdir /var/www/html/api
ADD api/*.py /var/www/html/api
RUN chmod +x /var/www/html/*.py

# Fix ownerships
RUN chown -R apache:apache /var/log/html && \
    chmod -R 660 /etc/pki/tls/certs/hosts.* && \
    chmod -R 660 /etc/pki/tls/private/hosts.key && \
    chown -R apache:apache /var/www/html && \
    chown -R apache:apache /var/log/httpd && \
    echo "export PYTHONPATH=/var/www/html/api:${PYTHONPATH}" >> /root/.bashrc

# We shouldn't have more than one API container running per host, so we'll go
# ahead and bind to the host's 443
EXPOSE 443

# Finally, fire up httpd
CMD ["-D", "FOREGROUND"]
ENTRYPOINT ["/usr/sbin/httpd"]

#END

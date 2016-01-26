# otoh.io API Specification

This is the API specification for otoh.io, the free, RESTful, certificate authority.

## Hostname

If you're using otoh.io as a service, assume that all URIs begin with https://api.otoh.io. If you're running on premisis, substitute with the FQDN of your otoh.io cluster's load balancer.

## Authenitcation

Most endpoints require a client certificate. See the table below for exceptions.

## Resources

Here's an index of the different API endpoints and their exposed methods.

| Description | Method | Endpoint | Authentication |
| :---------- | :----- | :------- | :------------- |
| Retrieve a CA certificate | GET | /ca | Client cert |
| Create a CA certificate | POST | /ca | Client cert |
| Delete a CA certificate | DELETE | /ca | Client cert |
| Retrieve a client or SSL certificate | GET | /cert | |
| Create a client or SSL certificate | POST | /cert | |
| Delete a client or SSL certificate | DELETE | /cert | Client cert |
| Submit a certificate signing request | POST | /csr | |
| Get an encrypted private key from escrow | GET | /escrow | Client cert |
| Submit an encrypted private key for escrow | POST | /escrow | Client cert |
| Update an encrypted private key already in escrow | PUT | /escrow | Client cert |
| Delete an encrypted private key already in escrow | DELETE | /escrow | Client cert |
| Get the status of a client or SSL certificate | GET | /ocsp | |
| Revoke a client or SSL certificate | POST | /ocsp | Client cert |
| Update a client or SSL certificate's validity | PUT | /ocsp | Client cert |
| Delete an OCSP entry for a client or SSL certificate | DELETE | /ocsp | Client cert |
| Search for a CA, client, or SSL certificate | POST | /search | |

## Endpoints

See the following sections for details on any endpoint.

### /ca

Retrieve and delete Certificate Authority certificates.

#### Example calls

| Method | Form | Example | JSON | Returns | Auth required |
| :----- | :------- | :------ | :----- | :------ | :----- |
| GET | /ca/<uuid> | https://api.otoh.io/ca/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | ```{ "ca": "<ca PEM>" }``` | None |
| POST | /ca | https://api.otoh.io/ca | ```{ "csr": "<csr PEM>" }``` | ```{ "uuid": "<uuid4>", "cert", "<cert PEM>" }``` | Client cert |
| DELETE | /ca/<uuid> | https://api.otoh.io/ca/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | None | Signing cert |

### /cert

Retrieve and delete client or SSL certificates.

#### Example calls

| Method | Form | Example | JSON | Returns | Auth required |
| :----- | :------- | :------ | :----- | :------ | :----- |
| GET | /cert/<uuid> | https://api.otoh.io/cert/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | ```{ "cert": "<cert PEM>" }``` | None |
| POST | /cert | https://api.otoh.io/cert | ```{ "csr": "<csr PEM>" }``` | ```{ "uuid": "<uuid4>", "cert", "<cert PEM>" }``` | None |
| DELETE | /cert/<uuid> | https://api.otoh.io/cert/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | None | Owning client cert, or signing cert |

### /csr

Submit certificate signing requests

#### Example calls

| Method | Form | Example | JSON | Returns | Auth required |
| :----- | :------- | :------ | :----- | :------ | :----- |
| POST | /csr | https://api.otoh.io/csr | ```{ "signing cert uuid": "<uuid4>", "usage": "{ke | ds | ssl | ca}", "csr": "<csr PEM>" }``` | ```{ "uiud": "<uuid4>", "cert": "<cert PEM>" }``` | None |

### /escrow

#### Example calls

| Method | Form | Example | JSON | Returns | Auth required |
| :----- | :------- | :------ | :----- | :------ | :----- |
| GET | /escrow/<uuid> | https://api.otoh.io/escrow/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | ```{ "key": "<cypher text>" }``` | Owning client cert, or signing cert |
| POST | /escrow | https://api.otoh.io/escrow | ```{ "signing cert sn": "<sn>", "cert sn": "<cert sn>", "key": "<cipher text>" }``` | ```{ "uuid": "<uuid4>" }``` | Owning client cert, or signing cert |
| PUT | /escrow/<uuid> | https://api.otoh.io/escrow/b787ce82-999f-4e39-afc0-c7a022a322a5 | ```{ "key": "<cipher text>" }``` | None | Owning client cert, or signing cert |
| DELETE | /escrow/<uuid> | https://api.otoh.io/escrow/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | None | Owning client cert, or signing cert |

### /ocsp

Get and manipulate certificate statuses for the Online Certificiate Status Protocol responder.

#### Example calls

| Method | Form | Example | JSON | Returns | Auth required |
| :----- | :------- | :------ | :----- | :------ | :----- |
| GET | /ocsp/<uuid> | https://api.otoh.io/ocsp/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | ```{ "certificate status": "valid | invalid | unknown", "signature": "<signature PEM>"}``` | None |
| POST | /ocsp | https://api.otoh.io/ocsp | ```{ "uuid": "<uuid4>", "status": "valid | invalid | unknown", "signature": "<signature PEM>" }``` | None | Owning client cert, or signing cert |
| PUT | /ocsp/<uuid> | https://api.otoh.io/ocsp/b787ce82-999f-4e39-afc0-c7a022a322a5 | ```{ "status": "{valid | invalid | unknown}", "signature": "<signature PEM>" }``` | None | Owning client cert, or signing cert |
| DELETE | /ocsp/<uuid> | https://api.otoh.io/ocsp/b787ce82-999f-4e39-afc0-c7a022a322a5 | None | None | Owning client cert, or signing cert |

### /search

Find a certificate's UUID.

#### Example calls

| Method | Form | Example | JSON | Returns | Auth required |
| :----- | :------- | :------ | :----- | :------ | :----- |
| GET | /search | https://api.otoh.io/search | ```{ "key": "{subjectName | email | fqdn}", "value": "foobar"}``` | ```{ "uuid": "<uuid4>"}``` | None |

#!/bin/bash

# Helper script for creating a self-signed certificate

# generate a private key
# openssl genrsa -des3 -out server.key 1024
openssl genrsa -aes256 -out server.key 4096

# generate the csr
openssl req -new -key server.key -out server.csr

# remove passphrase
cp server.key server.key.org && openssl rsa -in server.key.org -out server.key

# sign the cert
openssl x509 -sha512 -req -days 365 -in server.csr -signkey server.key -out server.crt

# result
openssl x509 -in server.crt -noout -text | grep 'Signature Algorithm' | head -1 | cut -d: -f2

# cleanup
rm server.csr server.key.org

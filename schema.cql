CREATE TABLE IF NOT EXISTS user (sn varchar, email varchar, account_status varchar, PRIMARY KEY (sn));
CREATE TABLE IF NOT EXISTS email (email varchar, user_sn varchar, verified timestamp, PRIMARY KEY (email));
CREATE TABLE IF NOT EXISTS user_cert (user_sn varchar, cert_sn varchar, PRIMARY KEY (user_sn));
CREATE TABLE IF NOT EXISTS cert (sn varchar, user_sn varchar, cert varchar, ca_chain varchar, PRIMARY KEY (sn));
CREATE TABLE IF NOT EXISTS ca (sn varchar, user_sn varchar, cert varchar, PRIMARY KEY (sn));
CREATE TABLE IF NOT EXISTS ca_cert (sn varchar, ca_sn varchar, cert_sn varchar, PRIMARY KEY (sn));
CREATE TABLE IF NOT EXISTS cert_ca (cert_sn varchar, ca_sn varchar, PRIMARY KEY (cert_sn));
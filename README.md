# Domain-2-CAA-proposal

Fetches Certificate Transparency results from certspotter and is able to filter, count, and list various aspects of the certificates. Ultimately it can output DNS CAA record configurations.


# Dependencies

* Python 3
* urlopen
* json
* pprint
* sys
* argparser
* collections


# Usage
```
usage: domain-2-CAA-proposal.py [-h] [--domain DOMAIN] [--caa]
                                [--matchissuer MATCHISSUER] [--issuer]
                                [--issuercount] [--uniqueissuers] [--dns]
                                [--caa-tips] [--out]

optional arguments:
  -h, --help            show this help message and exit
  --domain DOMAIN       Domain to scan.
  --caa                 Create a list of DNS CAA records based on the used
                        issuers.
  --matchissuer MATCHISSUER
                        Match to a specific issuer.
  --issuer              List all issuers.
  --issuercount         Count issuers.
  --uniqueissuers       List all issuers, only once.
  --dns                 Extract all Subject Alt Name DNS record from each
                        certificate and list them.
  --caa-tips            Tips on CAA configuration.
  --out                 Output all certificates in full.
```

# Sample output

## ./domain-2-CAA-proposal.py --domain koeroo.net --dns
```
domainhunter.koeroo.net
koeroo.com
koeroo.net
oscar.koeroo.com
oscar.koeroo.net
www.koeroo.com
www.koeroo.net
test.koeroo.net
tlsa.koeroo.net
domainhunter2.koeroo.net
cloud.koeroo.net
tlsa.koeroo.net
tlsa.koeroo.net
```

## ./domain-2-CAA-proposal.py --domain koeroo.net --issuer
```
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
```

## ./domain-2-CAA-proposal.py --domain koeroo.net --uniqueissuers
```
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
```

## ./domain-2-CAA-proposal.py --domain koeroo.net --issuercount
```
8      C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3
```

## ## ./domain-2-CAA-proposal.py --domain koeroo.net --uniqueissuers
```
C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3 
```

## ./domain-2-CAA-proposal.py --domain koeroo.net --caa-tips
```
= For reporting:
CAA 0 iodef "mailto:caa-reports@yourabusedesk.com"

= How to block a wildcard certificate in general:
CAA 0 issuewild ";"
```

## ./domain-2-CAA-proposal.py --domain koeroo.net --caa
```
CAA 0 issue "letsencrypt.org"
CAA 0 issuewild "letsencrypt.org"
```

## ./domain-2-CAA-proposal.py --domain koeroo.net --out
```
[   {   'data': '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',
        'dns_names': ['domainhunter.koeroo.net'],
        'issuer': "C=US, O=Let's Encrypt, CN=Let's Encrypt Authority X3",
        'logs': [   {   'id': 'pFASaQVaFVReYhGrN7wQP2KuVXakXksXFEU+GyIQaiU=',
                        'index': 364485605,
                        'timestamp': '2018-09-02T20:21:31.779-00:00'}],
        'not_after': '2018-12-01T19:21:31-00:00',
        'not_before': '2018-09-02T19:21:31-00:00',
        'pubkey_sha256': '188956e20e6609a783bfbd38cd264be58e89480d938f5dd378b4b76ef22cc050',
        'sha256': '99b771294c6848e1252ab31836b72aff61a1a532e9d2ce584c005c9759ffbae2',
        'type': 'cert'},
    {   'data': 'MIIHTTCCBjWgAwIBAgISA/GwMPqzlU0vb+9V0VmLJ+XFMA0GCSqGSIb3DQEBCwUAMEoxCzAJBgNVBAYTAlVTMRYwFAYDVQQKEw1MZXQncyBFbmNyeXB0MSMwIQYDVQQDExpMZXQncyBFbmNyeXB0IEF1dGhvcml0eSBYMzAeFw0xODA5MDIxOTIxMjVaFw0xODEyMDExOTIxMjVaMBUxEzARBgNVBAMTCmtvZXJvby5uZXQwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQDHNxXW6kIYHhqSIaBhFjnaatoNtvs8KN73xDpCLsdQV4zLbeSxv2gp6QxD/gqFyF1GlGLCnHiA7bEHKQoyITXF3Xqc4ng2nDczpxUJV8oW5AnINZCSaj8KTBTqFenJ1VJfHQeTllv/EcgLf/bliv80ULY8Gd27+DLZIQxcJSkCU5bz6rELJqvIwU1QNeN3O7gOxHr/4wekczjwZLjUOVQk698VfL+vP92EE3cysjcN/J8vhdZBXONEOQRzc7/A+k9yTg9UIdbLF5ZADWxqipNC++set2ueWhNqu6lMAAnarSHJE58l+dFGO3KieR/88JKopXJLWdQrbJx9FxgjtiJ5y/Hc1zLZBaAaips7ro0gP3wS/FijL83wQ54eib2DIH2u/ZFN9+nDqHa67x8mtEkWZPJtNKrvMXdR32RtXSbiu+05HYamZMif0hC7WaEYfw3k9F9lnhFQ2nQHPVZbI0ijT/v1LbZU ...
```

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

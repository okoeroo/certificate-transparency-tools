#!/usr/bin/env python3

from urllib.request import urlopen
import json
import pprint
import sys

domain = "kpn.com"

html = urlopen("https://certspotter.com/api/v0/certs?expired=false&duplicate=false&domain=" + domain)
res = json.loads(html.read())

pp = pprint.PrettyPrinter(indent=4)
#pp.pprint(res)


list = []

for ct_cert in res:
    print(ct_cert['issuer'])
    list.append(ct_cert['issuer'])


for ct_cert in res:
    for fqdn in ct_cert['dns_names']:
        print(fqdn)


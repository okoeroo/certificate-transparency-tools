#!/usr/bin/env python3

from urllib.request import urlopen
import json
import pprint
import sys
import argparse
import sys
from collections import Counter

def get_unique_issuers():
    l = []
    for ct_cert in res:
        l.append(ct_cert['issuer'])
    for i in sorted(set(l)):
        print(i)

def add_unique_to_dict_list(dict_list, key, value):
    for d in dict_list:
        if key in d:
            return d[key]

    # Work in progress
    dict_list.append({ key: value })
    return value


##################################################################################

parser = argparse.ArgumentParser("domain-2-CAA-proposal.py")
parser.add_argument("--domain", help="Domain to scan.", type=str)
parser.add_argument("--matchissuer", help="Match to a specific issuer.", type=str)
parser.add_argument('--issuer', default=False, action="store_true")
parser.add_argument('--issuercount', default=False, action="store_true")
parser.add_argument('--uniqueissuers', default=False, action="store_true")
parser.add_argument('--dns',  default=False, action="store_true")
parser.add_argument('--caa',  default=False, action="store_true")
parser.add_argument('--out', default=False, action="store_true")
args = parser.parse_args()


if args.domain is None:
    parser.print_help(sys.stderr)
    sys.exit(1)

#if not (args.issuer or args.dns or args.matchissuer):
#    parser.print_help(sys.stderr)
#    sys.exit(1)

# Fetch all data, seeve later
try:
    html = urlopen("https://certspotter.com/api/v0/certs?expired=false&duplicate=false&domain=" + args.domain).read().decode("utf-8")
    if html == None or len(html) == 0:
        print("Could not get data")
        sys.exit(1)
except Exception as e:
    sys.exit(1)

res = json.loads(html)
pp = pprint.PrettyPrinter(indent=4)

if args.out:
    pp.pprint(res)

if args.uniqueissuers:
    get_unique_issuers()

if args.issuer:
    # Print all issuers
    for ct_cert in res:
        print(ct_cert['issuer'])

if args.issuercount:
    l = []
    for ct_cert in res:
        l.append(ct_cert['issuer'])

    count_l = Counter(l)
    output_list= [] 

    for i in count_l:
        output_list.append([i, count_l[i]])

    for i in output_list:
        print(i[1], '\t', i[0])

if args.dns:
    for ct_cert in res:
        for fqdn in ct_cert['dns_names']:
            print(fqdn)

if args.matchissuer is not None:
    for ct_cert in res:
        if args.matchissuer in ct_cert['issuer']:
            pp.pprint(ct_cert)

if args.caa is not None:
    l = []
    for ct_cert in res:
        l.append(ct_cert['issuer'])

    got_this = []

    unique_issuers = sorted(set(l))

    for issuer_dn in unique_issuers:
        if "globalsign" in issuer_dn.lower():
            if "globalsign" in got_this:
                continue
            got_this.append("globalsign")
            print('CAA 0 issue "globalsign.com"')
            print('CAA 0 issuewild "globalsign.com"')
        elif "pkioverheid" in issuer_dn.lower() or "kpn" in issuer_dn.lower():
            if "pkioverheid" in got_this:
                continue
            got_this.append("pkioverheid")
            print('CAA 0 issue "kpn.com"')
        elif "digicert" in issuer_dn.lower():
            if "digicert" in got_this:
                continue
            got_this.append("digicert")
            print('CAA 0 issue "digicert.com"')
            print('CAA 0 issuewild "digicert.com"')
        elif "geotrust" in issuer_dn.lower():
            if "geotrust" in got_this:
                continue
            got_this.append("geotrust")
            print('CAA 0 issue "geotrust.com"')
            print('CAA 0 issuewild "geotrust.com"')
        elif "comodo" in issuer_dn.lower():
            if "comodo" in got_this:
                continue
            got_this.append("comodo")
            print('CAA 0 issue "comodoca.com"')
            print('CAA 0 issuewild "comodoca.com"')
        elif "amazon" in issuer_dn.lower():
            if "amazon" in got_this:
                continue
            got_this.append("amazon")
            print('CAA 0 issue "amazonaws.com"')
            print('CAA 0 issuewild "amazonaws.com"')
        else:
            print("-- No CAA config yet, apply for a support ticket", issuer_dn)



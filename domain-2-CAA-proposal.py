#!/usr/bin/env python3

from urllib.request import urlopen
import json
import pprint
import sys
import argparse
import sys

parser = argparse.ArgumentParser("domain-2-CAA-proposal.py")
parser.add_argument("--domain", help="Domain to scan.", type=str)
parser.add_argument("--matchissuer", help="Match to a specific issuer.", type=str)
parser.add_argument('--issuer', default=False, action="store_true")
parser.add_argument('--issuercount', default=False, action="store_true")
parser.add_argument('--uniqueissuers', default=False, action="store_true")
parser.add_argument('--dns',  default=False, action="store_true")
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

def get_unique_issuers():
    l = []
    for ct_cert in res:
        l.append(ct_cert['issuer'])
    for i in sorted(set(l)):
        print(i)

if args.uniqueissuers:
    get_unique_issuers()

if args.issuer:
    # Print all issuers
    for ct_cert in res:
        print(ct_cert['issuer'])

def add_unique_to_dict_list(dict_list, key, value):
    for d in dict_list:
        if key in d:
            return d[key]

    dict_list.append({ key: value })
    return value

if args.issuercount:
    l = []
    for ct_cert in res:
        # find
        l = add_unique_to_dict_list(l, 'issuer', ct_cert['issuer'])
        #if not any(l['issuer'] == ct_cert['issuer'] for d in a):


        d = {}
        d['issuer'] = ct_cert['issuer']
        d['count'] = 1
        l.append(ct_cert['issuer'])
    d = []

if args.dns:
    for ct_cert in res:
        for fqdn in ct_cert['dns_names']:
            print(fqdn)

if args.matchissuer is not None:
    for ct_cert in res:
        if args.matchissuer in ct_cert['issuer']:
            pp.pprint(ct_cert)

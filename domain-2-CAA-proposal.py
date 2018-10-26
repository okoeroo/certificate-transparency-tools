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
    return sorted(set(l))

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
parser.add_argument("--domain-file", help="File with domains to scan.", type=str)
parser.add_argument('--caa', help="Create a list of DNS CAA records based on the used issuers.", default=False, action="store_true")
parser.add_argument("--matchissuer", help="Match to a specific issuer.", type=str)
parser.add_argument('--issuer', help="List all issuers.", default=False, action="store_true")
parser.add_argument('--issuercount', help="Count issuers.", default=False, action="store_true")
parser.add_argument('--uniqueissuers', help="List all issuers, only once.", default=False, action="store_true")
parser.add_argument('--dns', help="Extract all Subject Alt Name DNS record from each certificate and list them.", default=False, action="store_true")
parser.add_argument('--caa-tips', help="Tips on CAA configuration.", default=False, action="store_true")
parser.add_argument('--out', help="Output all certificates in full.", default=False, action="store_true")
args = parser.parse_args()


if args.domain is None and args.domain_file is None and args.caa_tips is False:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.caa_tips:
    print("= For reporting:")
    print('CAA 0 iodef "mailto:caa-reports@yourabusedesk.com"')
    print()
    print("= How to block a wildcard certificate in general:")
    print('CAA 0 issuewild ";"')
    sys.exit(0)

#if not (args.issuer or args.dns or args.matchissuer):
#    parser.print_help(sys.stderr)
#    sys.exit(1)

if args.domain is not None:
    # Fetch all data, seeve later
    try:
        html = urlopen("https://certspotter.com/api/v0/certs?expired=false&duplicate=false&domain=" + args.domain).read().decode("utf-8")
        if html == None or len(html) == 0:
            print("Could not get data")
            sys.exit(1)
    except Exception as e:
        sys.exit(1)

    # The output
    res = json.loads(html)

if args.out:
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(res)

if args.uniqueissuers:
    l = get_unique_issuers()
    for i in l:
        print(i)

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

if args.caa:
    got_this = []
    unique_issuers = get_unique_issuers()

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
        elif "trust provider" in issuer_dn.lower():
            if "trust provider" in got_this:
                continue
            got_this.append("trust provider")
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
        elif "let's encrypt" in issuer_dn.lower():
            if "letsencrypt" in got_this:
                continue
            got_this.append("letsencrypt")
            print('CAA 0 issue "letsencrypt.org"')
            print('CAA 0 issuewild "letsencrypt.org"')
        elif "thawte" in issuer_dn.lower():
            if "thawte" in got_this:
                continue
            got_this.append("thawte")
            print('CAA 0 issue "thawte.com"')
            print('CAA 0 issuewild "thawte.com"')
        elif "symantec" in issuer_dn.lower():
            if "symantec" in got_this:
                continue
            got_this.append("symantec")
            print('CAA 0 issue "symantec.com"')
            print('CAA 0 issuewild "symantec.com"')
        elif "godaddy" in issuer_dn.lower():
            if "godaddy" in got_this:
                continue
            got_this.append("godaddy")
            print('CAA 0 issue "godaddy.com"')
            print('CAA 0 issuewild "godaddy.com"')
        elif "rapidssl" in issuer_dn.lower():
            if "rapidssl" in got_this:
                continue
            got_this.append("rapidssl")
            print('CAA 0 issue "rapidssl.com"')
            print('CAA 0 issuewild "rapidssl.com"')
        elif "certum" in issuer_dn.lower():
            if "certum" in got_this:
                continue
            got_this.append("certum")
            print('CAA 0 issue "certum.pl"')
            print('CAA 0 issuewild "certum.pl"')
        elif "goog" in issuer_dn.lower():
            if "goog" in got_this:
                continue
            got_this.append("goog")
            print('CAA 0 issue "pki.goog"')
            print('CAA 0 issuewild "pki.goog"')
        elif "entrust" in issuer_dn.lower():
            if "entrust" in got_this:
                continue
            got_this.append("entrust")
            print('CAA 0 issue "entrust.net"')
            print('CAA 0 issuewild "entrust.net"')
        elif "dfn" in issuer_dn.lower():
            if "dfn" in got_this:
                continue
            got_this.append("dfn")
            print('CAA 0 issue "pki.dfn.de"')
            print('CAA 0 issuewild "pki.dfn.de"')
        else:
            print("-- No CAA config yet, apply for a support ticket", issuer_dn)



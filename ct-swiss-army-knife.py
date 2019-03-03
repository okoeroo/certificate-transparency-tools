#!/usr/bin/env python3

import os
from urllib.request import urlopen
import json
import pprint
import sys
import argparse
import sys
import requests
import pprint
import csv
from collections import Counter

def get_unique_issuers(res):
    l = []
    for ct_cert in res:
        l.append(ct_cert['issuer']['name'])
    return sorted(set(l))

def add_unique_to_dict_list(dict_list, key, value):
    for d in dict_list:
        if key in d:
            return d[key]

    # Work in progress
    dict_list.append({ key: value })
    return value

def caatips():
    print("= For reporting:")
    print('CAA 0 iodef "mailto:caa-reports@yourabusedesk.com"')
    print()
    print("= How to block a wildcard certificate in general:")
    print('CAA 0 issuewild ";"')

def fetch_data_from_certspotter(domain, apikey):
    url = "".join(["https://api.certspotter.com/v1/issuances",
                "?",
                "domain=",
                domain,
                "&include_subdomains=true",
                "&match_wildcards=true",
                "&expired=false",
                "&expand=dns_names",
                "&expand=issuer"
                ])

    if apikey is None:
        r = requests.get(url)
    else:
        headers = {}
        headers['Authorization'] = " ".join(["Bearer", apikey])
        r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("Error:", r.status_code, domain, file=sys.stderr)
        print(r.text)
        return []

    # All ok, JSON result expected
    return r.json()

def fetch_certificates(search_domains, apikey):
#    1,000 single-hostname queries / hour => single certificate of one host
#    100 full-domain queries / hour => full domain is on.
#    75 queries / minute
#    5 queries / second

    search_results_json = []
    for domain in search_domains:
        search_results_json += fetch_data_from_certspotter(domain, apikey)

    return search_results_json

def main():
    parser = argparse.ArgumentParser("domain-2-CAA-proposal.py")
    parser.add_argument("--apikey",
                        dest='apikey',
                        type=str,
                        help="Cert Spotter API Key.")
    parser.add_argument("--stdin",
                        dest='stdin',
                        action="store_true",
                        help="File with domains to scan.")
    parser.add_argument("--dryrun",
                        dest='dryrun',
                        action="store_true",
                        help="Activates dry-run mode.")
    parser.add_argument("--domain-file",
                        dest='domainfile',
                        type=str,
                        help="File with domains to scan.")
    parser.add_argument('--caa',
                        default=False, 
                        action="store_true", 
                        help="Create a list of DNS CAA records based on the used issuers.")
    parser.add_argument('--uniqueissuers',
                        dest='uniqueissuers',
                        action="store_true",
                        help="List all issuers, only once.")
    parser.add_argument("--matchissuer",
                        type=str,
                        help="Match to a specific issuer.")
    parser.add_argument('--issuer',
                        action="store_true",
                        help="List all issuers.")
    parser.add_argument('--issuercount',
                        action="store_true",
                        help="Count issuers.")
    parser.add_argument('--dns',
                        action="store_true",
                        help="Extract all Subject Alt Name DNS record from each certificate and list them.")
    parser.add_argument('--caa-tips',
                        action="store_true",
                        help="Tips on CAA configuration.")
    parser.add_argument('--out',
                        action="store_true",
                        help="Output all certificates in full.")
    parser.add_argument('--csv',
                        dest='csvfile',
                        type=str,
                        help="Input file of type CSV.")
    parser.add_argument('--colnum',
                        dest='colnum',
                        type=int,
                        help="CSV file column number to use and it starts counting from zero")
    parser.add_argument('--delimiter',
                        dest='delimiter',
                        type=str,
                        help="CSV parser delimiter character")
    parser.add_argument('domains',
                        type=str,
                        nargs='*',
                        help='Domain(s) to scan.')
    args = parser.parse_args()

    # Only out some pointers/tips
    if args.caa_tips:
        caatips()
        sys.exit(0)

    # Parameter: input list
    search_domains = []

    # Domains via stdin per line
    if args.stdin:
        for line in sys.stdin:
            line = line.rstrip("\n").rstrip("\n\r").rstrip("\r\n").rstrip("\r")
            search_domains.append(line)

    # Domains via positional input on the CLI
    for i in args.domains:
        search_domains.append(i)

    # Domains via file input
    if args.domainfile and os.path.exists(args.domainfile):
        f = open(args.domainfile, "r")
        for line in f.readlines():
            line = line.rstrip("\n").rstrip("\n\r").rstrip("\r\n").rstrip("\r")
            search_domains.append(line)

    # Domains via CSV file input
    if args.csvfile and os.path.exists(args.csvfile):
        if args.delimiter is None or args.colnum is None:
            print("Error: must specify a delimiter and colomn number when using the CSV file input", file=sys.stderr)
            sys.exit(1)

        with open(args.csvfile) as f:
            csvreader_web_loc = csv.reader(f, delimiter=args.delimiter)
            for row in csvreader_web_loc:
                search_domains.append(row[args.colnum])

    # Check: no input, no dice => bailing
    if len(search_domains) == 0:
        print("Error: No domains provided as input.", file=sys.stderr)
        sys.exit(1)

    # Dry-run?
    if args.dryrun:
        for i in search_domains:
            print(i)
        sys.exit(0)

    # Fetch certificates from CT logs and build JSON output
    certs_json = fetch_certificates(search_domains, args.apikey)

    # Output
    if args.out:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(certs_json)

    if args.uniqueissuers:
        l = get_unique_issuers(certs_json)
        for i in l:
            print(i)

    if args.issuer:
        # Print all issuers
        for ct_cert in certs_json:
            print(ct_cert['issuer']['name'])

    if args.issuercount:
        l = []
        for ct_cert in certs_json:
            l.append(ct_cert['issuer']['name'])

        count_l = Counter(l)
        output_list= [] 

        for i in count_l:
            output_list.append([i, count_l[i]])

        for i in output_list:
            print(i[1], '\t', i[0])

    if args.dns:
        for ct_cert in certs_json:
            for fqdn in ct_cert['dns_names']:
                print(fqdn)

    if args.matchissuer is not None:
        for ct_cert in certs_json:
            if args.matchissuer in ct_cert['issuer']:
                pp.pprint(ct_cert)

    if args.caa:
        got_this = []
        unique_issuers = get_unique_issuers(certs_json)

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




##################################################################################
if __name__ == "__main__":
    main()


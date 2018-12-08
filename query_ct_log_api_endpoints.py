#!/usr/bin/env python3

import requests
import json

ctl_log = requests.get('https://www.gstatic.com/ct/log_list/log_list.json', timeout=5).json()

total_certs = 0
for log in ctl_log['logs']:
    log_url = log['url']
    try:
        print(log_url)
        log_info = requests.get('https://{}/ct/v1/get-sth'.format(log_url), timeout=3).json()
        total_certs += int(log_info['tree_size'])

        print(log_url, int(log_info['tree_size']), total_certs)
    except:
        continue



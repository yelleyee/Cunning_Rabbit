import requests
import pprint
import setting

def set_dns(new_ip):

    payload = {
        "comment": "VPN",
        "name": setting.cf_record_name,
        "proxied": False,
        "settings": {},
        "tags": [],
        "ttl": 60,
        "content": new_ip,
        "type": "A"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": setting.cf_auth 
    }

    response = requests.request("PUT", setting.cf_dns_instance_url, json=payload, headers=headers)

    pprint.pprint(response.text)


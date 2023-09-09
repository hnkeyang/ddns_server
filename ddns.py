import threading
import json
import os
from dns_server import DNS_Server
from update_api import Update_API

os.chdir(os.path.split(os.path.realpath(__file__))[0])

DOMAIN_IP_MAP = {}
AUTH_TOKEN_MAP = {
    '3beacceac4252f5da3428dcdba4ae215': ['1.ddns.com'],
    '3beacceac4252f5da3428dcdba4ae214': []
}

host = '127.0.0.1'
dns_port = 53
api_port = 2053

def start_dns_server():
    dns = DNS_Server(host=host, port=dns_port, domain_ip_map=DOMAIN_IP_MAP)
    dns.run()

def start_api():
    api = Update_API(host=host, port=api_port, domain_ip_map=DOMAIN_IP_MAP, auth_token_map=AUTH_TOKEN_MAP)
    api.run()


with open('domain_ip.json') as f:
    DOMAIN_IP_MAP = json.load(f)

dns_thread = threading.Thread(target=start_dns_server)
dns_thread.start()

start_api()

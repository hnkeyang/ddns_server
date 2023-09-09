from bottle import Bottle, request, response
import json


class Update_API:
    def __init__(self, host=None, port=None, domain_ip_map={}, auth_token_map={}):
        self.host = host
        self.port = port
        self.domain_ip_map = domain_ip_map
        self.auth_token_map = auth_token_map

        self.app = Bottle()
        self.route()

    def route(self):
        self.app.route('/update', method='GET', callback=self.update_ip)

    def update_ip(self):
        token = request.query.token
        domain = request.query.domain
        ip = request.query.ip or request.remote_addr

        if token not in self.auth_token_map or (len(self.auth_token_map[token]) != 0 and domain not in self.auth_token_map[token]):
            return 'Unauthorized'

        if domain not in self.domain_ip_map or self.domain_ip_map[domain] != ip:
            self.domain_ip_map[domain] = ip

            with open('domain_ip.json', 'w') as f:
                json.dump(self.domain_ip_map, f)

            return 'Update success'

        return 'IP unchanged'

    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == '__main__':

    DOMAIN_IP_MAP = {}
    AUTH_TOKEN_MAP = {
        '3beacceac4252f5da3428dcdba4ae215': ['1.ddns.com'],
        '3beacceac4252f5da3428dcdba4ae214': []
    }


    # with open('domain_ip.json') as f:
    #     DOMAIN_IP_MAP = json.load(f)
    api = Update_API(host='127.0.0.1', port=8080, domain_ip_map=DOMAIN_IP_MAP, auth_token_map=AUTH_TOKEN_MAP)
    api.run()
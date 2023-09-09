from dnslib import DNSRecord, DNSHeader, RR, A, QTYPE
from socket import socket, AF_INET, SOCK_DGRAM
import json


class DNS_Server:
    def __init__(self, host=None, port=None, domain_ip_map={}):
        self.host = host
        self.port = port
        self.domain_ip_map = domain_ip_map

    def dns_response(self, request):
        reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q) 

        qname = request.q.qname
        qn = str(qname).strip('.')

        if qn in self.domain_ip_map and request.q.qtype == QTYPE.A:
            ip = self.domain_ip_map[qn]
            reply.add_answer(RR(qname, rtype=request.q.qtype, rdata=A(ip), ttl=300))

        return reply

    def run(self):
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        udp_socket.bind((self.host, self.port))

        while True:
            data, addr = udp_socket.recvfrom(512)
            request = DNSRecord.parse(data)
            reply = self.dns_response(request)

            if reply.rr:
                udp_socket.sendto(reply.pack(), addr)

if __name__ == '__main__':

    DOMAIN_IP_MAP = {
        'www.example.com': '1.2.3.4', 
        'test.example.com': '127.0.0.1'
    }

    DOMAIN_IP_MAP = {}

#    with open('domain_ip.json', 'w') as f:
#        json.dump(DOMAIN_IP_MAP, f)

    with open('domain_ip.json') as f:
        DOMAIN_IP_MAP = json.load(f)

    IP = '127.0.0.1'
    PORT = 53 

    dns = DNS_Server(host=IP, port=PORT, domain_ip_map=DOMAIN_IP_MAP)
    dns.run()

from scapy.all import *
import subprocess
from scapy.layers.dns import DNS
from scapy.layers.inet import *


class ProxyManager(object):
    """
    This module is responsible for all the operations related to forwarding the DNS requests to the actual
    DNS server, in case needed
    """

    def __init__(self, configuration_file_path = 'dnsproxy_config'):
        """
        :param configuration_file_path: A string representing the path to the dnsproxy configuration file.
        """
        self._configuration_file_path = configuration_file_path

    def run_dnsproxy_daemon(self):
        """
        This method runs the dnsproxy tool which should recieve DNS requests and forwarding them to the
        actual DNS server
        """
        subprocess.call('sudo dnsproxy -c {}'.format(self._configuration_file_path), shell=True)

    def redirect_dns_query(self, pkt):
        ip = pkt[IP]
        udp = pkt[UDP]
        dns = pkt[DNS]
        udp.dst = str(1025)
        send(ip/udp/dns)

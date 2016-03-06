import socket
import os
import netifaces
import ipaddress
import time
import logging
from multiprocessing.pool import ThreadPool

from homebrain import Agent, Event, Dispatcher

class DeviceMonitor(Agent):

    autostart = True

    def __init__(self, target=None, netmask=24):
        super(DeviceMonitor, self).__init__()
        # Initialize values
        self.target = target if target is not None else self.identifier
        self.dispatcher = Dispatcher()
        self.threadpool = ThreadPool(5)
        self.updateinterval = 30
        self._known_devices = {}
        # Fetch network device IPs
        default_gateway = netifaces.gateways()['default']
        if (default_gateway):
            (gateway_ip, interface) = default_gateway[netifaces.AF_INET]
            self.network = ipaddress.ip_network('%s/%d' % (gateway_ip, netmask), False)
        else:
            logging.error("DeviceMonitor couldn't start, no default gateway available")
            self.stop()

    def run(self):
        start_time = time.time()
        available_devices = set()

        while self._enabled:
            # Get current local network devices
            current_devices = self._get_active_devices()
            # Filter out new and lost devices
            new_devices = current_devices - available_devices
            lost_devices = available_devices - current_devices

            for (ip, hostname) in new_devices:
                data = {'data': {'status': 'connected', 'hostname': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                self._known_devices[hostname] = {'ip': ip, 'hostname': hostname, 'status': True, 'ports':[]}

            for (ip, hostname) in lost_devices:
                data = {'data': {'status': 'disconnected', 'hostname': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                self._known_devices[hostname]['status'] = False

            # Update available devices
            available_devices = current_devices

            # Check all devices open homebrain ports
            openports = self._get_open_ports()
            for item in openports:
                # Get past values
                device = self._known_devices[item[0]]
                currentports = item[1]
                prevports = set(device["ports"])
                # Filter out new and lost ports
                newports = set(currentports)-prevports
                lostports = set(prevports)-set(currentports)
                if newports:
                    logging.info("New homebrain node(s) from '{}' available: {}".format(device["hostname"], str(newports)))
                if lostports:
                    logging.info("Homebrain node(s) from '{}' is now unavailable: {}".format(device["hostname"], str(lostports)))
                # Update to new ports
                device["ports"] = currentports

            # Wait for the next update interval
            while start_time + self.updateinterval > time.time():
                time.sleep(1)
            start_time = time.time()

    def _get_active_devices(self):
        hosts = list(map(lambda h: str(h), self.network.hosts()))
        devices = self.threadpool.map(_is_active, hosts)
        return set(filter(None, devices))

    def _get_open_ports(self):
        hosts = list(map(lambda h: str(h), self._known_devices))
        portdevices = self.threadpool.map(_ports_open, hosts)
        return portdevices

    @property
    def known_devices(self):
        return self._known_devices

def _is_active(ip):
    # Ping device to see if it is alive
    try:
        (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(ip)
        response = os.system("ping -c 1 -t 1 " + ip + " > /dev/null 2>&1")
        if response == 0:
            return (ip, hostname)
    except socket.herror:
        pass
    return None

def _ports_open(ip):
    # Get all open HomeBrain ports from devices
    ports = []
    for port in range(5602, 5610):
        if _port_is_open(ip, port):
            ports.append(port)
    return (ip, ports)

def _port_is_open(ip, port):
    # Check open port on device
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = 1
    try:
        result = sock.connect_ex((ip,port))
    except socket.gaierror as e:
        pass
    if result == 0:
        return True
    else:
        return False

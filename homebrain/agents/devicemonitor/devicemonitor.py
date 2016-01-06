import socket
import os
import netifaces
import ipaddress
import time
import logging
from multiprocessing.pool import ThreadPool

from homebrain import Agent, Event, Dispatcher

class DeviceMonitor(Agent):
    def __init__(self, target=None, netmask=24):
        super(DeviceMonitor, self).__init__()
        self.target = target if target is not None else self.identifier
        self.dispatcher = Dispatcher()
        self.updateinterval = 30

        default_gateway = netifaces.gateways()['default']
        if (default_gateway):
            (gateway_ip, interface) = default_gateway[netifaces.AF_INET]
            self.network = ipaddress.ip_network('%s/%d' % (gateway_ip, netmask), False)
        else:
            logging.error("DeviceMonitor couldn't start, no default gateway available")
            self.stop()
        self._known_devices = {}
        self._connected_devices = set()

    def run(self):
        start_time = time.time()
        while self._enabled:
            current_devices = self._get_active_devices()
            connected_devices = current_devices - self._connected_devices
            disconnected_devices = self._connected_devices - current_devices

            for (ip, hostname) in connected_devices:
                data = {'data': {'status': 'connected', 'hostname': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                self._known_devices[hostname] = {'ip': ip, 'hostname': hostname, 'status': True, 'ports':[]}
                #logging.info('device_connection: '+str(self._known_devices[hostname]))

            for (ip, hostname) in disconnected_devices:
                data = {'data': {'status': 'disconnected', 'hostname': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                self._known_devices[hostname]['status'] = False
                #logging.info('device_connection: '+str(data))

            self._connected_devices = current_devices
            openports = self._get_open_ports()
            for item in openports:
                device = self._known_devices[item[0]]
                currentports = item[1]
                prevports = set(device["ports"])
                newports = set(currentports)-prevports
                oldports = set(prevports)-set(currentports)
                if newports:
                    logging.info("New homebrain port from '{}' available: {}".format(device["hostname"], str(newports)))
                if oldports:
                    logging.info("Homebrain port from '{}' is now unavailable: {}".format(device["hostname"], str(oldports)))
                device["ports"] = currentports

            while start_time + self.updateinterval > time.time():
                time.sleep(1)
            start_time = time.time()

    def _get_active_devices(self):
        pool = ThreadPool(5)
        hosts = list(map(lambda h: str(h), self.network.hosts()))
        devices = pool.map(_is_active, hosts)
        return set(filter(None, devices))

    def _get_open_ports(self):
        pool = ThreadPool(5)
        hosts = list(map(lambda h: str(h), self._known_devices))
        portdevices = pool.map(_ports_open, hosts)
        return portdevices

    @property
    def known_devices(self):
        return self._known_devices

def _is_active(ip):
    try:
        (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(ip)
        return (ip, hostname)
    except socket.herror:
        return None

def _ports_open(ip):
    #print(ip)
    ports = []
    for port in range(5602, 5610):
        if _port_is_open(ip, port):
            ports.append(port)
    return (ip, ports)

def _port_is_open(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((ip,port))
    if result == 0:
        return True
    else:
        return False

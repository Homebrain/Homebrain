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

        default_gateway = netifaces.gateways()['default']
        if (default_gateway):
            (gateway_ip, interface) = default_gateway[netifaces.AF_INET]
            self.network = ipaddress.ip_network('%s/%d' % (gateway_ip, netmask), False)
        else:
            logging.log(logging.ERROR, "DeviceMonitor couldn't start, no default gateway available")
            self.stop()
        self._known_devices = set()
        self._connected_devices = set()

    def run(self):
        while self._enabled:
            time.sleep(5)
            current_devices = self._get_active_devices()
            connected_devices = current_devices - self._connected_devices
            disconnected_devices = self._connected_devices - current_devices

            for (ip, hostname) in connected_devices:
                data = {'data': {'status': 'connected', 'hostname': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                logging.log(logging.INFO, 'device_connection: '+str(data))

            for (ip, hostname) in disconnected_devices:
                data = {'data': {'status': 'disconnected', 'hostname': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                logging.log(logging.INFO, 'device_connection: '+str(data))

            self._known_devices = set(list(self._known_devices) + list(current_devices))
            self._connected_devices = current_devices

    def _get_active_devices(self):
        pool = ThreadPool(5)
        hosts = list(map(lambda h: str(h), self.network.hosts()))
        devices = pool.map(_is_active, hosts)
        return set(filter(None, devices))

    @property
    def known_devices(self):
        devices = {}
        for item in self._known_devices:
            connected = False
            if item in self._connected_devices:
                connected = True
            devices[item[1]] = {'ip': item[0], 'hostname':item[1], 'status': connected}
        return devices

def _is_active(ip):
    try:
        (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(ip)
        return (ip, hostname)
    except socket.herror:
        return None

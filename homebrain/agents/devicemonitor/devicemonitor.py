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

    def run(self):
        known_devices = set()
        while self._enabled:
            time.sleep(5)
            current_devices = self._active_devices()
            connected_devices = current_devices - known_devices
            disconnected_devices = known_devices - current_devices

            for (ip, hostname) in connected_devices:
                data = {'data': {'action': 'connected', 'device': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                logging.log(logging.INFO, 'device_connection: '+str(data))

            for (ip, hostname) in disconnected_devices:
                data = {'data': {'action': 'disconnected', 'device': hostname}}
                self.dispatcher.put_event(Event(type='device_connection', data=data))
                logging.log(logging.INFO, 'device_connection: '+str(data))

            known_devices = current_devices

    def _active_devices(self):
        pool = ThreadPool(5)
        hosts = list(map(lambda h: str(h), self.network.hosts()))
        devices = pool.map(_is_active, hosts)
        return set(filter(None, devices))

def _is_active(ip):
    try:
        (hostname, aliaslist, ipaddrlist) = socket.gethostbyaddr(ip)
        return (ip, hostname)
    except socket.herror:
        return None

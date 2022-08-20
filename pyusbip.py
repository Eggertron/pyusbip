import argparse
import logging
import os
from subprocess import check_output
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class UsbIpServer():
    def __init__(self):
        self.start_daemon()
    
    def start_daemon(self):
        stdout = check_output(["usbipd", "-D"]).decode()
        return stdout.split('\n')

    def get_devices_list(self):
        result = list()
        stdout = check_output("lsusb").decode()
        for line in stdout.split('\n'):
            if not line:
                continue
            lane, id = line.split(':', maxsplit=1)
            lanes = lane.split()
            ids = id.strip().split(' ', maxsplit=2)
            hash = {
                "Bus": lanes[1],
                "Device": lanes[3],
                "ID": ids[1],
                "Description": ids[2]
            }
            result.append(hash)
        return result

    def get_bus_id(self, usbid:str):
        stdout = check_output(["usbip", "list", "-p", "-l"]).decode()
        for line in stdout.split('\n'):
            if not line:
                continue
            if usbid in line:
                kv, _ = line.split('#', maxsplit=1)
                return kv.split('=')[1]
        return None

    def bind_bus_id(self, busid:str):
        try:
            stdout = check_output(["usbip", "bind", f"--busid={busid}"]).decode()
        except Exception as e:
            logging.error(e)
            stdout = e.stdout
        return stdout

class UsbIp():
    def __init__(self, usbip_server=None, usbip_path=None):
        if usbip_path:
            self.usbip_path = usbip_path
        if usbip_server:
            self.usbip_server = usbip_server

    def validate_modules(self):
        usbip_core = "usbip_core"
        vhci_hcd = "vhci_hcd"
        result = True
        stdout = check_output("lsmod").decode()
        logging.debug(f"stdout type {type(stdout)}")
        for module in (usbip_core, vhci_hcd):
            if module not in stdout:
                print(f"Looks like {module} is not loaded.")
                result = False
        return result

    def load_modules(self):
        if self.validate_modules():
            print("Modules already loaded.")
            return
        usbip_core = "usbip-core"
        vhci_hcd = "vhci-hcd"
        for module in (usbip_core, vhci_hcd):
            cmd = ["sudo", "modprobe", module]
            check_output(cmd)
        if self.validate_modules():
            print("Modules loaded successfully.")
        else:
            print("Failed to load modules.")

    def get_version(self):
        cmd = [self.usbip_path, "version"]
        return check_output(cmd).decode()

    def list_connected(self):
        cmd = ["sudo", self.usbip_path, "port"]
        return check_output(cmd).decode()

    def list_devices(self):
        cmd = ["sudo", self.usbip_path, "list", "-r", self.usbip_server]
        return check_output(cmd).decode()
    
    def attach_device(self, bus_id):
        cmd = [self.usbip_path, "attach", "-r", self.usbip_server, "-b", bus_id]
        return check_output(cmd).decode()

    def detach_device(self, port_id):
        cmd = [self.usbip_path, "detach", "-p", port_id]
        return check_output(cmd).decode()


logging.basicConfig(level=logging.DEBUG)
# current path for my ubuntu
#usbip_path = os.path.join(os.sep, "usr", "lib", "linux-tools-5.4.0-104", "usbip")
#usbip_path = os.path.join(os.sep, "usr", "sbin", "usbip")

#usbip = UsbIp(usbip_server="192.168.50.250", usbip_path=usbip_path)
#usbip.load_modules()
#print(usbip.get_version())
#print(usbip.list_devices())
#print(usbip.list_connected())

u = UsbIpServer()
print(u.get_devices_list())
print(u.bind_bus_id(u.get_bus_id("045e:0294")))

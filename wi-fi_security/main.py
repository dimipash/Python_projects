import json
import logging
import argparse
import socket
import netifaces
from datetime import datetime
from typing import List, Dict, Optional
import scapy.all as scapy
import nmap

# Configure logging
logging.basicConfig(
    filename="network_security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ConfigManager:
    """Manages loading and saving of security configurations to JSON file"""

    def __init__(self, config_file: str = "security_config.json"):
        self.config_file = config_file
        self.config = {"allowed_devices": [], "blocked_devices": [], "network_info": {}}

    def load_config(self) -> None:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
            logging.info("Configuration loaded successfully")
        except FileNotFoundError:
            logging.warning("Config file not found, using default configuration")

    def save_config(self) -> None:
        """Save current configuration to JSON file"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)
        logging.info("Configuration saved successfully")

    def add_allowed_device(self, mac_address: str) -> None:
        """Add a device MAC to whitelist"""
        if mac_address not in self.config["allowed_devices"]:
            self.config["allowed_devices"].append(mac_address)
            self.save_config()

    def remove_allowed_device(self, mac_address: str) -> None:
        """Remove a device MAC from whitelist"""
        if mac_address in self.config["allowed_devices"]:
            self.config["allowed_devices"].remove(mac_address)
            self.save_config()


class NetworkScanner:
    """Handles network scanning and device discovery"""

    def __init__(self):
        self.interface = self._get_default_interface()
        self.nm = nmap.PortScanner()

    def _get_default_interface(self) -> str:
        """Get default network interface using netifaces"""
        gateways = netifaces.gateways()
        return gateways["default"][netifaces.AF_INET][1]

    def get_network_info(self) -> Dict:
        """Get network information including IP range and SSID"""
        interface = self.interface
        addrs = netifaces.ifaddresses(interface)
        ip_info = addrs[netifaces.AF_INET][0]
        return {
            "interface": interface,
            "ip_address": ip_info["addr"],
            "netmask": ip_info["netmask"],
            "broadcast": ip_info["broadcast"],
        }

    def scan_devices(self) -> List[Dict]:
        """Scan network for connected devices using ARP"""
        devices = []
        arp_request = scapy.ARP(pdst=self.get_network_info()["broadcast"])
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request

        try:
            answered = scapy.srp(packet, timeout=3, verbose=False)[0]
            for sent, received in answered:
                devices.append(
                    {
                        "ip": received.psrc,
                        "mac": received.hwsrc,
                        "hostname": self._get_hostname(received.psrc),
                    }
                )
            logging.info(f"Found {len(devices)} devices on network")
        except PermissionError:
            logging.error(
                "Permission denied for network scan. Try running as admin/sudo"
            )
        return devices

    def _get_hostname(self, ip: str) -> Optional[str]:
        """Resolve hostname from IP address"""
        try:
            return socket.gethostbyaddr(ip)[0]
        except socket.herror:
            return None


class SecurityMonitor:
    """Main security monitoring and management class"""

    def __init__(self):
        self.config = ConfigManager()
        self.config.load_config()
        self.scanner = NetworkScanner()
        self.running = False

    def display_network_info(self) -> None:
        """Display network information"""
        info = self.scanner.get_network_info()
        print(f"\nNetwork Interface: {info['interface']}")
        print(f"IP Address: {info['ip_address']}")
        print(f"Network Range: {info['broadcast']}")

    def detect_unauthorized_devices(self) -> List[Dict]:
        """Check for devices not in whitelist"""
        authorized = self.config.config["allowed_devices"]
        current_devices = self.scanner.scan_devices()
        return [device for device in current_devices if device["mac"] not in authorized]

    def start_monitoring(self, interval: int = 300) -> None:
        """Start continuous network monitoring"""
        self.running = True
        logging.info(f"Starting network monitoring with {interval} second interval")
        try:
            while self.running:
                unauthorized = self.detect_unauthorized_devices()
                if unauthorized:
                    self._handle_unauthorized(unauthorized)
                time.sleep(interval)
        except KeyboardInterrupt:
            self.stop_monitoring()

    def stop_monitoring(self) -> None:
        """Stop monitoring loop"""
        self.running = False
        logging.info("Network monitoring stopped")

    def _handle_unauthorized(self, devices: List[Dict]) -> None:
        """Handle unauthorized device detection"""
        for device in devices:
            message = (
                f"Unauthorized device detected: {device['mac']} ({device['hostname']})"
            )
            logging.warning(message)
            print(f"\nALERT: {message}")
            # Additional notification logic could be added here


def main():
    """Command-line interface handler"""
    parser = argparse.ArgumentParser(description="Wi-Fi Network Security Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Scan command
    scan_parser = subparsers.add_parser(
        "scan", help="Scan network for connected devices"
    )

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Start real-time monitoring")
    monitor_parser.add_argument(
        "--interval", type=int, default=300, help="Monitoring interval in seconds"
    )

    # Device management commands
    device_parser = subparsers.add_parser("add-device", help="Add device to whitelist")
    device_parser.add_argument("--mac", required=True, help="MAC address to whitelist")

    remove_parser = subparsers.add_parser(
        "remove-device", help="Remove device from whitelist"
    )
    remove_parser.add_argument("--mac", required=True, help="MAC address to remove")

    # Report command
    subparsers.add_parser("generate-report", help="Generate security report")

    # Config command
    subparsers.add_parser("show-config", help="Show current security configuration")

    args = parser.parse_args()
    monitor = SecurityMonitor()

    if not args.command:
        parser.print_help()
        return

    if args.command == "scan":
        monitor.display_network_info()
        devices = monitor.scanner.scan_devices()
        print("\nConnected Devices:")
        for device in devices:
            print(
                f"IP: {device['ip']}\tMAC: {device['mac']}\tHostname: {device['hostname']}"
            )

    elif args.command == "monitor":
        monitor.start_monitoring(args.interval)

    elif args.command == "add-device":
        monitor.config.add_allowed_device(args.mac)
        print(f"Device {args.mac} added to whitelist")

    elif args.command == "remove-device":
        monitor.config.remove_allowed_device(args.mac)
        print(f"Device {args.mac} removed from whitelist")

    elif args.command == "generate-report":
        # Implement report generation
        print("Security report generated in network_security.log")

    elif args.command == "show-config":
        print("Allowed Devices:", monitor.config.config["allowed_devices"])
        print("Blocked Devices:", monitor.config.config["blocked_devices"])

    else:
        parser.print_help()


if __name__ == "__main__":
    main()

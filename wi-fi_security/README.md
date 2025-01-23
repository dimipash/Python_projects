# Wi-Fi Network Security Tool

A Python-based network security utility for monitoring and managing devices on your Wi-Fi network.

## Features

-   Network device discovery and scanning
-   Real-time unauthorized device detection
-   MAC address whitelist management
-   Continuous network monitoring with configurable intervals
-   Detailed logging of security events
-   Command-line interface (CLI) for easy operation
-   Configuration persistence through JSON file

## Requirements

-   Python 3.8+
-   Windows OS (Tested on Windows 11)

## Installation

1. Clone this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py [command] [options]

Available commands:
  scan                Scan network for connected devices
  monitor             Start real-time monitoring
  add-device          Add device to whitelist
  remove-device       Remove device from whitelist
  generate-report     Generate security report
  show-config         Show current security configuration

Options:
  --help              Show help message and exit
```

### Example Commands

-   Scan network devices:

```bash
python main.py scan
```

-   Start monitoring with 5-minute interval:

```bash
python main.py monitor --interval 300
```

-   Whitelist a device:

```bash
python main.py add-device --mac 00:1A:2B:3C:4D:5E
```

-   Remove device from whitelist:

```bash
python main.py remove-device --mac 00:1A:2B:3C:4D:5E
```

## Configuration

Security settings are stored in `security_config.json`:

-   `allowed_devices`: List of trusted MAC addresses
-   `blocked_devices`: List of blocked MAC addresses (reserved for future use)
-   `network_info`: Automatically detected network parameters

The configuration file is automatically created on first run and persists between sessions.

## Dependencies

-   scapy (Packet manipulation)
-   netifaces (Network interface detection)
-   python-nmap (Port scanning capabilities)
-   argparse (Command-line parsing)

## Troubleshooting

**Permission Errors:**

```bash
# Run with administrative privileges if needed
python main.py scan
```

**Missing Dependencies:**

```bash
# Ensure all requirements are installed
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! Please open an issue or PR for any improvements.

## License

MIT License

## Acknowledgements

-   scapy community for powerful network packet manipulation
-   nmap project for network discovery capabilities

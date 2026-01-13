#!/usr/bin/env python
"""
Example: Using device attributes in simulations

This script demonstrates how to use device attributes when running simulations
via the HTTP API.
"""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def example_1_default_attributes():
    """
    Example 1: Default attributes (admin_user=True for all devices)
    - All devices can spread malware
    - Fastest spread
    """
    print("=" * 70)
    print("Example 1: Default Attributes")
    print("=" * 70)
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free"
            # No device_attributes specified - uses defaults
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 100
    }
    
    print("Request: Using default device attributes")
    print(f"Network: 50 nodes, scale-free topology")
    print(f"All devices: admin_user=True (normal spread)")
    
    # Make request (requires API running on localhost:8000)
    # response = requests.post(f"{API_BASE_URL}/api/v1/simulate", json=payload)
    print("\n✓ Would run with default attributes allowing normal spread\n")


def example_2_restricted_spread():
    """
    Example 2: Most devices cannot spread (admin_user=False)
    - Simulates restricted user accounts
    - Only devices with admin privileges can spread
    """
    print("=" * 70)
    print("Example 2: Restricted Spread (Most devices have admin_user=False)")
    print("=" * 70)
    
    payload = {
        "network_config": {
            "num_nodes": 100,
            "network_type": "scale_free",
            "device_attributes": {
                "device_type": "workstation",
                "admin_user": False  # Restrict spread to only admin users
            }
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 100
    }
    
    print("Request: Restrict malware spread")
    print(f"Network: 100 nodes, scale-free topology")
    print(f"All devices: admin_user=False (cannot spread to neighbors)")
    print("Impact: Much slower spread, malware contained better")
    
    print("\n✓ Would run with limited spread capability\n")


def example_3_server_network():
    """
    Example 3: Server environment with security measures
    - All servers are patched and have antivirus
    - Can still be infected but represents better-protected environment
    """
    print("=" * 70)
    print("Example 3: Protected Server Environment")
    print("=" * 70)
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free",
            "device_attributes": {
                "device_type": "server",
                "os": "Windows Server 2019",
                "patch_status": "patched",
                "firewall_enabled": True,
                "antivirus": True,
                "admin_user": True
            }
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 100
    }
    
    print("Request: Protected server environment")
    print(f"Network: 50 nodes, scale-free topology")
    print(f"All devices:")
    print(f"  - Type: server")
    print(f"  - OS: Windows Server 2019")
    print(f"  - Patch Status: patched")
    print(f"  - Firewall: enabled")
    print(f"  - Antivirus: enabled")
    print(f"  - Admin User: yes")
    print("Future logic could use these attributes to reduce infection rates")
    
    print("\n✓ Would run with well-protected environment\n")


def example_4_mixed_environment():
    """
    Example 4: Realistic mixed environment
    Shows how to set different attributes per node using the API
    (Note: Currently API applies same attributes to all nodes.
     Individual node setup would be done programmatically)
    """
    print("=" * 70)
    print("Example 4: Mixed Environment (Programmatic Setup)")
    print("=" * 70)
    
    print("""
from network_model import NetworkGraph
from malware_engine.malware_base import Worm
from simulation import Simulator

# Create a mixed environment network
network = NetworkGraph(network_type="scale_free")
network.generate_topology(100, device_attributes={
    "admin_user": True  # Default for all
})

# Set up different device types
# Servers (patched, protected)
for i in range(0, 10):
    network.set_device_attributes(f"device_{i}",
        device_type="server",
        os="Windows Server 2019",
        patch_status="patched",
        firewall_enabled=True,
        antivirus=True
    )

# Critical servers (even more protected, no admin spread)
for i in range(10, 15):
    network.set_device_attributes(f"device_{i}",
        device_type="server",
        os="Windows Server 2019",
        patch_status="patched",
        firewall_enabled=True,
        antivirus=True,
        admin_user=False  # Critical servers isolated
    )

# User workstations (less protected)
for i in range(15, 100):
    network.set_device_attributes(f"device_{i}",
        device_type="workstation",
        os="Windows 10",
        patch_status="unpatched",  # Some users don't patch
        firewall_enabled=False,
        antivirus=False
    )

# Run simulation
malware = Worm("worm_1", infection_rate=0.35, latency=1)
simulator = Simulator(network, malware)
simulator.initialize(["device_0"])
simulator.run(max_steps=100)

# Analyze results
stats = simulator.get_statistics()
print(f"Infected: {stats['total_infected']}/{stats['total_devices']} nodes")
    """)
    
    print("✓ This creates a realistic mixed environment\n")


def example_5_api_with_device_attributes():
    """
    Example 5: Full HTTP API request with WebSocket
    """
    print("=" * 70)
    print("Example 5: WebSocket with Device Attributes")
    print("=" * 70)
    
    ws_url = "ws://localhost:8000/ws/simulate"
    
    config = {
        "network_config": {
            "num_nodes": 100,
            "network_type": "scale_free",
            "device_attributes": {
                "device_type": "server",
                "patch_status": "patched",
                "admin_user": True
            }
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 100
    }
    
    print(f"WebSocket Connection: {ws_url}")
    print(f"Configuration:")
    print(json.dumps(config, indent=2))
    
    print("""
# Python WebSocket client example
import asyncio
import websockets
import json

async def run():
    async with websockets.connect('ws://localhost:8000/ws/simulate') as ws:
        # Send config with device attributes
        await ws.send(json.dumps(config))
        
        # Receive real-time updates
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            
            if data['type'] == 'step':
                print(f"Step {data['step']}: {data['newly_infected']} new infections")
            elif data['type'] == 'complete':
                print(f"Done! {data['statistics']['total_infected']} infected")
                break

asyncio.run(run())
    """)
    
    print("✓ WebSocket streaming with device attributes\n")


if __name__ == "__main__":
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + "Device Attributes Examples".center(68) + "║")
    print("║" + "MSpreadEngine API Usage".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    example_1_default_attributes()
    example_2_restricted_spread()
    example_3_server_network()
    example_4_mixed_environment()
    example_5_api_with_device_attributes()
    
    print("=" * 70)
    print("Key Points:")
    print("=" * 70)
    print("1. Device attributes are stored in network nodes")
    print("2. Default admin_user=True maintains backward compatibility")
    print("3. Attributes can be set at topology generation or per-device")
    print("4. Future logic can use attributes to modify infection behavior")
    print("5. API supports device_attributes in network_config")
    print("=" * 70)
    print()

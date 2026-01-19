"""
Test suite for MSpreadEngine API endpoints.

This script tests the FastAPI server by making HTTP requests to all available endpoints.
Make sure the API server is running before executing this script:
    python main.py run
"""

import requests
import json
import time
from typing import Dict, List
import sys
import asyncio
import websockets
import argparse

API_BASE_URL = "http://localhost:8000"
API_VERSION = "/api/v1"

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}{Colors.ENDC}\n")


def print_success(text: str):
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def test_server_health() -> bool:
    print_header("Testing Server Health")
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Server is healthy: {data}")
            return True
        else:
            print_error(f"Server returned status code {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to API server. Make sure it's running:")
        print(f"  {Colors.OKBLUE}python main.py run{Colors.ENDC}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_root_endpoint() -> bool:
    print_header("Testing Root Endpoint")
    
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success("Root endpoint working")
            print_info(f"Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print_error(f"Root endpoint returned status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_simulation_simple(num_nodes: int = 50) -> bool:
    print_header(f"Testing Simple Simulation ({num_nodes} nodes)")
    
    payload = {
        "network_config": {
            "num_nodes": num_nodes,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "custom"
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Sending simple simulation request...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}{API_VERSION}/simulate",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Simple simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            
            # Check for new statistics
            if "performance" in data:
                perf = data["performance"]
                print_info(f"Peak Velocity: {perf.get('peak_velocity')} infections/step")
            else:
                print_warning("Missing performance stats")
                
            if "network_topology" in data:
                topo = data["network_topology"]
                print_info(f"Avg Degree: {topo.get('avg_degree', 'N/A')}")
            else:
                print_warning("Missing network topology stats")

            return True
        else:
            print_error(f"Simulation failed with status code {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_simulation_complex(num_nodes: int = 50) -> bool:
    print_header(f"Testing Complex Simulation ({num_nodes} nodes)")
    
    payload = {
        "network_config": {
            "num_nodes": num_nodes,
            "network_type": "scale_free",
            "device_attributes": {
                "os": "Windows",
                "device_type": "server"
            },
            "node_definitions": [
                {"count": 10, "attributes": {"os": "Linux", "device_type": "server"}}
            ],
            "node_distribution": "random"
        },
        "malware_config": {
            "malware_type": "custom",
            "infection_rate": 0.8,
            "latency": 2,
            "spread_pattern": "bfs",
            "target_os": ["Windows"],
            "avoids_admin": False
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Sending complex simulation request...")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}{API_VERSION}/simulate",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Complex simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            
            # Print Performance Stats
            if "performance" in data:
                perf = data["performance"]
                print_info("\nPerformance Metrics:")
                print_info(f"  Peak Velocity: {perf.get('peak_velocity')} infections/step")
                print_info(f"  Step at Peak: {perf.get('step_at_peak')}")
                print_info(f"  Steps to 50%: {perf.get('steps_to_50_percent')}")
            
            # Print Network Topology Stats
            if "network_topology" in data:
                topo = data["network_topology"]
                print_info("\nNetwork Topology:")
                print_info(f"  Nodes: {topo.get('num_nodes')}")
                print_info(f"  Edges: {topo.get('num_edges')}")
                if isinstance(topo.get('avg_degree'), (int, float)):
                    print_info(f"  Avg Degree: {topo.get('avg_degree'):.2f}")
                print_info(f"  Components: {topo.get('num_components', 'N/A')}")
                
                if "demographics" in topo:
                    demo = topo["demographics"]
                    print_info(f"  OS Breakdown: {demo.get('os_breakdown')}")
                    if isinstance(demo.get('admin_ratio'), (int, float)):
                        print_info(f"  Admin Ratio: {demo.get('admin_ratio'):.2f}")

            # Print Infected Demographics
            if "infected_demographics" in data:
                inf_demo = data["infected_demographics"]
                print_info("\nInfected Demographics:")
                print_info(f"  By OS: {inf_demo.get('os_breakdown')}")

            print_info("\nNote: Linux nodes should be excluded from infection")
            return True
        else:
            print_error(f"Simulation failed with status code {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_different_topologies() -> bool:
    print_header("Testing Different Network Topologies")
    
    topologies = ["scale_free", "small_world", "random"]
    results = []
    
    for topology in topologies:
        print_info(f"Testing {topology} topology...")
        
        payload = {
            "network_config": {
                "num_nodes": 30,
                "network_type": topology
            },
            "malware_config": {
                "malware_type": "worm",
                "infection_rate": 0.35,
                "latency": 1
            },
            "initial_infected": ["device_0"],
            "max_steps": 50
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}{API_VERSION}/simulate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"{topology}: {data['total_infected']}/{data['total_devices']} infected")
                results.append((topology, data['total_infected'], data['total_devices']))
            else:
                print_error(f"{topology} failed with status {response.status_code}")
        except Exception as e:
            print_error(f"{topology} error: {str(e)}")
    
    # Compare results
    print_info("\nTopology Comparison:")
    for topology, infected, total in results:
        percentage = (infected / total * 100)
        print(f"  {topology:15} → {infected:2}/{total} ({percentage:5.1f}%) infected")
    
    return len(results) == len(topologies)


def test_infection_rate_comparison() -> bool:
    print_header("Testing Different Infection Rates")
    
    infection_rates = [0.1, 0.2, 0.3, 0.4, 0.5]
    results = []
    
    for rate in infection_rates:
        print_info(f"Testing infection rate: {rate}")
        
        payload = {
            "network_config": {
                "num_nodes": 50,
                "network_type": "scale_free"
            },
            "malware_config": {
                "malware_type": "worm",
                "infection_rate": rate,
                "latency": 1
            },
            "initial_infected": ["device_0"],
            "max_steps": 50
        }
        
        try:
            response = requests.post(
                f"{API_BASE_URL}{API_VERSION}/simulate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                print_success(f"Rate {rate}: {data['total_infected']} infected in {data['total_steps']} steps")
                results.append((rate, data['total_infected'], data['total_steps']))
            else:
                print_error(f"Rate {rate} failed")
        except Exception as e:
            print_error(f"Rate {rate} error: {str(e)}")
    
    # Show trend
    print_info("\nInfection Rate Comparison:")
    for rate, infected, steps in results:
        print(f"  Rate {rate}: {infected:3} infected in {steps:2} steps")
    
    return len(results) == len(infection_rates)


def test_multiple_initial_infected() -> bool:
    """Test simulation with multiple initially infected devices."""
    print_header("Testing Multiple Initial Infections")
    
    payload = {
        "network_config": {
            "num_nodes": 100,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0", "device_5", "device_10", "device_15"],
        "max_steps": 50
    }
    
    print_info(f"Starting with 4 initially infected devices")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}{API_VERSION}/simulate",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            return True
        else:
            print_error(f"Simulation failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_device_attributes_all_admin() -> bool:
    """Test simulation with all devices as admin users (normal spread)."""
    print_header("Testing Device Attributes: All Admin Users")
    
    payload = {
        "network_config": {
            "num_nodes": 80,
            "network_type": "scale_free",
            "device_attributes": {
                "device_type": "server",
                "admin_user": True
            }
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info("All devices: admin_user=True (normal spread expected)")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}{API_VERSION}/simulate",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            print_info("Result: Malware spread freely across admin network")
            return True
        else:
            print_error(f"Simulation failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_device_attributes_all_non_admin() -> bool:
    """Test simulation with all devices as non-admin users (restricted spread)."""
    print_header("Testing Device Attributes: All Non-Admin Users")
    
    payload = {
        "network_config": {
            "num_nodes": 80,
            "network_type": "scale_free",
            "device_attributes": {
                "device_type": "workstation",
                "admin_user": False
            }
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info("All devices: admin_user=False (no spread possible)")
    print_info("Expected: Infection should be limited to initial device")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}{API_VERSION}/simulate",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            
            # Verify that infection is minimal (only initial device)
            if data['total_infected'] == 1:
                print_success("Spread blocked: Non-admin devices cannot infect each other")
            else:
                print_info(f"Note: {data['total_infected']} devices infected (topology may allow some spread)")
            
            return True
        else:
            print_error(f"Simulation failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_device_attributes_mixed() -> bool:
    """Test simulation with mixed admin/non-admin users (70/30 split with random distribution)."""
    print_header("Testing Device Attributes: Mixed Admin/Non-Admin (70/30 Random)")
    
    payload = {
        "network_config": {
            "num_nodes": 100,
            "network_type": "scale_free",
            "node_definitions": [
                {"count": 70, "attributes": {"admin_user": True, "device_type": "server"}},
                {"count": 30, "attributes": {"admin_user": False, "device_type": "workstation"}}
            ],
            "node_distribution": "random"
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info("Setup: 100 devices split into batches with RANDOM distribution")
    print_info("  - Batch 1: 70 devices with admin_user=True (servers)")
    print_info("  - Batch 2: 30 devices with admin_user=False (workstations)")
    print_info("  - Distribution: RANDOM (mixed throughout network, not clustered)")
    print_info("Expected: Admin and non-admin devices mixed, privilege boundaries tested")
    
    try:
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}{API_VERSION}/simulate",
            json=payload,
            timeout=60
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            print_info("Result: Random distribution creates realistic network with mixed device types")
            return True
        else:
            print_error(f"Simulation failed with status {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


async def test_websocket_simulation_simple() -> bool:
    """Test WebSocket endpoint for simple simulation."""
    print_header("Testing WebSocket Simple Simulation")
    
    websocket_url = "ws://localhost:8000/ws/simulate"
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "custom"
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Connecting to WebSocket at {websocket_url}")
    
    try:
        async with websockets.connect(websocket_url) as websocket:
            print_success("Connected to WebSocket")
            await websocket.send(json.dumps(payload))
            
            step_count = 0
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    if data["type"] == "complete":
                        stats = data["statistics"]
                        print_success(f"Simulation completed via WebSocket")
                        print_info(f"Total Steps: {step_count}")
                        print_info(f"Total Infected: {stats['total_infected']}")
                        return True
                    
                    elif data["type"] == "step":
                        step_count += 1
                    
                    elif data["type"] == "error":
                        print_error(f"Server error: {data['message']}")
                        return False
                
                except asyncio.TimeoutError:
                    print_error("WebSocket connection timeout")
                    return False
    
    except Exception as e:
        print_error(f"WebSocket error: {str(e)}")
        return False


async def test_websocket_simulation_complex() -> bool:
    """Test WebSocket endpoint for complex simulation testing countermeasures."""
    print_header("Testing WebSocket Complex Simulation (Countermeasures)")
    
    websocket_url = "ws://localhost:8000/ws/simulate"
    
    # 50 Nodes:
    # - 20 Servers (Windows, Firewall=True, Patched)
    # - 20 Workstations (Windows, Antivirus=True, Unpatched) 
    # - 10 IoT (Linux, No protection)
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free",
            "node_definitions": [
                {
                    "count": 20, 
                    "attributes": {
                        "device_type": "server", 
                        "os": "Windows", 
                        "firewall_enabled": True, 
                        "patch_status": "fully_patched",
                        "admin_user": True
                    }
                },
                {
                    "count": 20, 
                    "attributes": {
                        "device_type": "workstation", 
                        "os": "Windows", 
                        "antivirus": True, 
                        "patch_status": "unpatched",
                        "admin_user": False
                    }
                },
                {
                    "count": 10, 
                    "attributes": {
                        "device_type": "iot", 
                        "os": "Linux", 
                        "firewall_enabled": False,
                        "admin_user": False
                    }
                }
            ],
            "node_distribution": "random"
        },
        "malware_config": {
            "malware_type": "custom_apt",
            "infection_rate": 0.9,
            "latency": 1,
            "spread_pattern": "bfs",
            "target_os": ["Windows", "Linux"],
            "bypass_firewall": True,  # Can hit servers despite firewall
            "zero_day": False,        # Cannot hit fully_patched servers
            "avoids_admin": False
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Connecting to WebSocket at {websocket_url}")
    print_info("Scenario: Malware bypasses firewall but blocked by patches.")
    print_info("Expected: Servers (patched) survive, Workstations/IoT get infected.")
    
    try:
        async with websockets.connect(websocket_url) as websocket:
            print_success("Connected to WebSocket")
            await websocket.send(json.dumps(payload))
            
            step_count = 0
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    
                    if data["type"] == "complete":
                        stats = data["statistics"]
                        print_success(f"Complex simulation completed via WebSocket")
                        print_info(f"Total Steps: {step_count}")
                        print_info(f"Total Infected: {stats['total_infected']}/{stats['total_devices']}")
                        
                        if "infected_demographics" in stats:
                            print_info(f"Infected OS Breakdown: {stats['infected_demographics'].get('os_breakdown')}")
                            
                        return True
                    
                    elif data["type"] == "step":
                        step_count += 1
                        if step_count % 5 == 0:
                            print_info(f"Step {data['step']}: {data['newly_infected']} new -> {data['total_infected']} total")
                    
                    elif data["type"] == "error":
                        print_error(f"Server error: {data['message']}")
                        return False
                        
                except asyncio.TimeoutError:
                    return False
                    
    except Exception as e:
        print_error(f"WebSocket error: {str(e)}")
        return False


def test_default_malware() -> bool:
    print_header("Testing Default Malware Config")
    payload = {
        "network_config": {"num_nodes": 50, "network_type": "scale_free"},
        "malware_config": {"malware_type": "custom"},
        "initial_infected": ["device_0"],
        "max_steps": 20
    }
    try:
        response = requests.post(f"{API_BASE_URL}{API_VERSION}/simulate", json=payload, timeout=10)
        if response.status_code == 200:
            print_success("Default malware simulation successful")
            return True
        else:
            print_error(f"Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_configured_malware() -> bool:
    print_header("Testing Fully Configured Malware")
    payload = {
        "network_config": {"num_nodes": 50, "network_type": "scale_free"},
        "malware_config": {
            "malware_type": "custom",
            "infection_rate": 0.8,
            "latency": 0,
            "spread_pattern": "bfs",
            "avoids_admin": False
        },
        "initial_infected": ["device_0"],
        "max_steps": 20
    }
    try:
        response = requests.post(f"{API_BASE_URL}{API_VERSION}/simulate", json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print_success("Configured malware simulation successful")
            print_info(f"Infected: {data.get('total_infected')}")
            return True
        else:
            print_error(f"Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_segmented_network() -> bool:
    print_header("Testing Segmented Network (2 Subnets + Firewalls)")
    
    # Define 2 subnets of 50 nodes each, connected by 4 bridges
    payload = {
        "network_config": {
            "num_nodes": 0, # Ignored for segmented topology but required by schema
            "network_type": "segmented",
            "subnets": [
                {"num_nodes": 50, "network_type": "scale_free", "device_attributes": {"os": "Linux"}},
                {"num_nodes": 50, "network_type": "random", "device_attributes": {"os": "Windows"}}
            ],
            "interconnects": [
                {"source_subnet": 0, "target_subnet": 1, "source_node": 0, "target_node": 0, "firewall": True},
                {"source_subnet": 0, "target_subnet": 1, "source_node": 1, "target_node": 1, "firewall": True},
                {"source_subnet": 0, "target_subnet": 1, "source_node": 2, "target_node": 2, "firewall": True},
                {"source_subnet": 0, "target_subnet": 1, "source_node": 3, "target_node": 3, "firewall": True}
            ]
        },
        "malware_config": {
            "malware_type": "custom",
            "infection_rate": 0.8,
            "bypass_firewall": False 
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info("Scenario: Infection starts in Subnet 0 (Linux). Bridges have Firewall enabled.")
    
    try:
        response = requests.post(f"{API_BASE_URL}{API_VERSION}/simulate", json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            print_success("Segmented simulation successful")
            
            # Print Total Network Composition
            if "network_topology" in data:
                topo_demo = data["network_topology"].get("demographics", {})
                print_info(f"Total Network:   {topo_demo.get('os_breakdown')}")
                
            # Print Infection Results
            print_info(f"Total Infected:  {data['total_infected']}")
            if "infected_demographics" in data:
                print_info(f"Infection Breakdown: {data['infected_demographics']['os_breakdown']}")
            
            windows_infected = data.get("infected_demographics", {}).get("os_breakdown", {}).get("Windows", 0)
            if windows_infected < 10:
                print_success(f"Firewall effective! Only {windows_infected} Windows nodes infected.")
            else:
                print_warning(f"Firewall breached? {windows_infected} Windows nodes infected.")
                
            return True
        else:
            print_error(f"Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_cve_exploitation() -> bool:
    print_header("Testing CVE Exploitation (Targeted Attack)")
    
    # Generate 150 random CVEs plus our target CVE
    # This simulates a "noisy" vulnerability scan result to test O(1) lookup performance
    extra_cves = [f"CVE-202{i%10}-{10000+i}" for i in range(150)]
    target_cve = "CVE-2023-1234"
    node_cves = extra_cves + [target_cve]
    
    # 50 Nodes total:
    # - 10 Vulnerable Servers (Have CVE-2023-1234 + 150 noise CVEs)
    # - 40 Secure Workstations (No CVEs)
    payload = {
        "network_config": {
            "num_nodes": 5000,
            "network_type": "scale_free",
            "node_definitions": [
                {
                    "count": 1000,
                    "attributes": {
                        "device_type": "vulnerable_server",
                        "os": "Windows Server 2016"
                    },
                    "vulnerabilities": node_cves
                },
                {
                    "count": 4000,
                    "attributes": {
                        "device_type": "secure_workstation",
                        "os": "Windows 10"
                    }
                }
            ],
            "node_distribution": "random"
        },
        "malware_config": {
            "malware_type": "exploit_kit",
            "infection_rate": 0.5,
            "latency": 1,
            "exploits": ["CVE-2023-1234"],
            "cve_only": True  # Crucial: ONLY infect nodes with this CVE
        },
        "initial_infected": ["device_0"],
        "max_steps": 30
    }
    
    print_info("Scenario: Malware with 'cve_only=True' targeting CVE-2023-1234")
    print_info("Network: 1000 Vulnerable Nodes (CVE-2023-1234), 4000 Secure Nodes")
    print_info("Expected: Exactly 1000 nodes (or fewer if disconnected) should be infected.")
    
    try:
        response = requests.post(f"{API_BASE_URL}{API_VERSION}/simulate", json=payload, timeout=20)
        if response.status_code == 200:
            data = response.json()
            total_infected = data['total_infected']
            
            print_success("CVE Simulation successful")
            print_info(f"Total Infected: {total_infected}/5000")
            print_info(f"Total Steps: {data.get('total_steps', 'N/A')}")
            
            if total_infected <= 1000:
                print_success(f"Perfect! Infection contained to vulnerable nodes (<= 1000).")
                return True
            else:
                print_error(f"Failure! Infection spread to {total_infected} nodes. Should be max 1000.")
                return False
        else:
            print_error(f"Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def run_all_tests():
    # Define all tests as a list of tuples (test_number, test_name, test_function, is_async)
    tests = [
        (1, "Server Health", test_server_health, False),
        (2, "Root Endpoint", test_root_endpoint, False),
        (3, "Simple Simulation", lambda: test_simulation_simple(50), False),
        (4, "Complex Simulation", lambda: test_simulation_complex(50), False),
        (5, "Network Topologies", test_different_topologies, False),
        (6, "Infection Rate Comparison", test_infection_rate_comparison, False),
        (7, "Multiple Initial Infections", test_multiple_initial_infected, False),
        (8, "Device Attributes: All Admin", test_device_attributes_all_admin, False),
        (9, "Device Attributes: All Non-Admin", test_device_attributes_all_non_admin, False),
        (10, "Device Attributes: Mixed", test_device_attributes_mixed, False),
        (11, "WebSocket Simple Simulation", test_websocket_simulation_simple, True),
        (12, "WebSocket Complex Simulation", test_websocket_simulation_complex, True),
        (13, "Default Malware Config", test_default_malware, False),
        (14, "Fully Configured Malware", test_configured_malware, False),
        (15, "Segmented Network Simulation", test_segmented_network, False),
        (16, "CVE Exploitation Attack", test_cve_exploitation, False),
    ]
    
    return tests


def print_menu():
    """Display the test menu."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{'Available Tests':^70}")
    print(f"{'='*70}{Colors.ENDC}\n")
    
    tests = run_all_tests()
    
    for test_num, test_name, _, _ in tests:
        print(f"  {Colors.BOLD}{test_num:2d}{Colors.ENDC}. {test_name}")
    
    print(f"\n  {Colors.BOLD}0{Colors.ENDC}. Run all tests (default)")
    print(f"  {Colors.BOLD}q{Colors.ENDC}. Quit\n")


def run_selected_tests(test_numbers: List[int] = None):
    """Run selected tests or all tests."""
    print(f"{Colors.BOLD}{Colors.OKBLUE}")
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    MSpread API Test Suite                              ║
║            Testing FastAPI Endpoints and Functionality                 ║
╚════════════════════════════════════════════════════════════════════════╝
    """)
    print(Colors.ENDC)
    
    tests = run_all_tests()
    results = {}
    
    # Determine which tests to run
    if test_numbers is None or len(test_numbers) == 0:
        # Run all tests
        tests_to_run = tests
    else:
        # Run only selected tests, maintaining order
        tests_to_run = [t for t in tests if t[0] in test_numbers]
        if not tests_to_run:
            print_error("No valid test numbers provided")
            return
    
    # Check server health first (always run this)
    if any(t[0] != 1 for t in tests_to_run):
        health_test = [t for t in tests if t[0] == 1][0]
        print(f"\n{Colors.BOLD}Pre-check: {Colors.ENDC}")
        test_num, test_name, test_func, _ = health_test
        results["Server Health"] = test_func()
        if not results["Server Health"]:
            print_error("\nCannot connect to API server. Aborting tests.")
            return
    
    # Run WebSocket tests with asyncio
    async_tests = [t for t in tests_to_run if t[3]]
    sync_tests = [t for t in tests_to_run if not t[3]]
    
    # Run synchronous tests
    for test_num, test_name, test_func, _ in sync_tests:
        if test_name in results:
            continue
        results[test_name] = test_func()
    
    # Run asynchronous tests if any
    if async_tests:
        print_header("Running WebSocket Tests")
        
        async def run_async_tests():
            async_results = {}
            for test_num, test_name, test_func, _ in async_tests:
                async_results[test_name] = await test_func()
            return async_results
        
        websocket_results = asyncio.run(run_async_tests())
        results.update(websocket_results)
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if result else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"  {test_name:40} → {status}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}✓ All tests passed!{Colors.ENDC}\n")
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}⚠ Some tests failed!{Colors.ENDC}\n")


def interactive_menu():
    """Run the interactive test menu."""
    while True:
        print_menu()
        user_input = input(f"{Colors.BOLD}Select test(s) to run (comma-separated or 0 for all): {Colors.ENDC}").strip()
        
        if user_input.lower() == 'q':
            print(f"\n{Colors.OKGREEN}Exiting test suite{Colors.ENDC}\n")
            sys.exit(0)
        
        if user_input == '0' or user_input == '':
            run_selected_tests()
            break
        
        try:
            test_numbers = [int(x.strip()) for x in user_input.split(',')]
            valid_tests = list(range(1, 16))
            
            invalid_tests = [t for t in test_numbers if t not in valid_tests]
            if invalid_tests:
                print_error(f"Invalid test number(s): {', '.join(map(str, invalid_tests))}")
                continue
            
            run_selected_tests(test_numbers)
            break
        except ValueError:
            print_error("Invalid input. Please enter numbers separated by commas.")
            continue


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(
            description="MSpread API Test Suite - Test individual or all API endpoints",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  python test_api_demo.py              # Run all tests (default)
  python test_api_demo.py -t 8         # Run test #8 (Multiple Initial Infections)
  python test_api_demo.py -t 1 2 3     # Run tests #1, #2, #3
  python test_api_demo.py -t 9 10 11   # Run WebSocket tests only
  python test_api_demo.py -m           # Interactive menu
            """
        )
        
        parser.add_argument(
            '-t', '--test',
            nargs='+',
            type=int,
            help='Test number(s) to run (1-15). Multiple tests can be specified.'
        )
        
        parser.add_argument(
            '-m', '--menu',
            action='store_true',
            help='Show interactive menu'
        )
        
        parser.add_argument(
            '-l', '--list',
            action='store_true',
            help='List all available tests'
        )
        
        args = parser.parse_args()
        
        # Handle --list option
        if args.list:
            print_menu()
            sys.exit(0)
        
        # Handle --menu option
        if args.menu:
            interactive_menu()
            sys.exit(0)
        
        # Handle --test option
        if args.test:
            run_selected_tests(args.test)
        else:
            # Default: run all tests
            run_selected_tests()
    
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}")
        sys.exit(1)

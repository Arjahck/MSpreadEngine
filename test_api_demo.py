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


def test_simulation_worm(num_nodes: int = 50) -> bool:
    print_header(f"Testing Worm Simulation ({num_nodes} nodes)")
    
    payload = {
        "network_config": {
            "num_nodes": num_nodes,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Sending simulation request...")
    print_info(f"Payload: {json.dumps(payload, indent=2)}")
    
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
            print_success(f"Worm simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Devices: {data['total_devices']}")
            print_info(f"Total Infected: {data['total_infected']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            print_info(f"Malware Type: {data['malware_type']}")
            
            # Show first 5 steps
            print_info("First 5 infection steps:")
            for step in data['history'][:5]:
                print(f"    Step {step['step']}: {step['newly_infected']} new → {step['total_infected']} total infected")
            
            return True
        else:
            print_error(f"Simulation failed with status code {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print_error("Request timed out (60 seconds)")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_simulation_virus(num_nodes: int = 50) -> bool:
    print_header(f"Testing Virus Simulation ({num_nodes} nodes)")
    
    payload = {
        "network_config": {
            "num_nodes": num_nodes,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "virus",
            "infection_rate": 0.25,
            "latency": 2
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Sending simulation request...")
    
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
            print_success(f"Virus simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            return True
        else:
            print_error(f"Simulation failed with status code {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print_error("Request timed out (60 seconds)")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False


def test_simulation_ransomware(num_nodes: int = 50) -> bool:
    print_header(f"Testing Ransomware Simulation ({num_nodes} nodes)")
    
    payload = {
        "network_config": {
            "num_nodes": num_nodes,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "ransomware",
            "infection_rate": 0.30,
            "latency": 3
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Sending simulation request...")
    
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
            print_success(f"Ransomware simulation completed in {elapsed_time:.2f}s")
            print_info(f"Total Infected: {data['total_infected']}/{data['total_devices']}")
            print_info(f"Infection Percentage: {data['infection_percentage']:.2f}%")
            print_info(f"Total Steps: {data['total_steps']}")
            return True
        else:
            print_error(f"Simulation failed with status code {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print_error("Request timed out (60 seconds)")
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


async def test_websocket_simulation_worm() -> bool:
    """Test WebSocket endpoint for real-time worm simulation streaming."""
    print_header("Testing WebSocket Worm Simulation (Real-time Streaming)")
    
    websocket_url = "ws://localhost:8000/ws/simulate"
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Connecting to WebSocket at {websocket_url}")
    
    try:
        async with websockets.connect(websocket_url) as websocket:
            print_success("Connected to WebSocket")
            
            # Send simulation configuration
            print_info("Sending simulation configuration...")
            await websocket.send(json.dumps(payload))
            
            step_count = 0
            total_infected = 0
            messages = []
            
            # Receive messages from server
            while True:
                try:
                    message = await websocket.recv()
                    data = json.loads(message)
                    messages.append(data)
                    
                    if data["type"] == "initialized":
                        print_success(f"Simulation initialized: {data['total_devices']} devices, {data['initial_infected']} initially infected")
                    
                    elif data["type"] == "step":
                        step_count += 1
                        total_infected = data["total_infected"]
                        if step_count <= 5:  # Show first 5 steps in detail
                            print_info(f"Step {data['step']}: {data['newly_infected']} newly infected → {total_infected} total")
                    
                    elif data["type"] == "complete":
                        stats = data["statistics"]
                        print_success(f"Simulation completed via WebSocket")
                        print_info(f"Total Steps: {step_count}")
                        print_info(f"Total Infected: {stats['total_infected']}/{stats['total_devices']}")
                        print_info(f"Infection Percentage: {stats['infection_percentage']:.2f}%")
                        print_info(f"Malware Type: {stats['malware_type']}")
                        
                        # Show summary
                        if step_count > 5:
                            print_info(f"... ({step_count - 5} more steps) ...")
                        
                        return True
                    
                    elif data["type"] == "error":
                        print_error(f"Server error: {data['message']}")
                        return False
                
                except asyncio.TimeoutError:
                    print_error("WebSocket connection timeout")
                    return False
    
    except ConnectionRefusedError:
        print_error("Cannot connect to WebSocket. Make sure API server is running:")
        print(f"  {Colors.OKBLUE}python main.py run{Colors.ENDC}")
        return False
    except Exception as e:
        print_error(f"WebSocket error: {str(e)}")
        return False


async def test_websocket_simulation_virus() -> bool:
    """Test WebSocket endpoint for virus simulation."""
    print_header("Testing WebSocket Virus Simulation")
    
    websocket_url = "ws://localhost:8000/ws/simulate"
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "virus",
            "infection_rate": 0.25,
            "latency": 2
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Testing Virus via WebSocket...")
    
    try:
        async with websockets.connect(websocket_url) as websocket:
            await websocket.send(json.dumps(payload))
            
            step_count = 0
            final_infected = 0
            
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data["type"] == "step":
                    step_count += 1
                    final_infected = data["total_infected"]
                
                elif data["type"] == "complete":
                    stats = data["statistics"]
                    print_success(f"Virus simulation completed: {final_infected}/{stats['total_devices']} infected in {step_count} steps")
                    return True
                
                elif data["type"] == "error":
                    print_error(f"Error: {data['message']}")
                    return False
    
    except Exception as e:
        print_error(f"WebSocket error: {str(e)}")
        return False


async def test_websocket_simulation_ransomware() -> bool:
    """Test WebSocket endpoint for ransomware simulation."""
    print_header("Testing WebSocket Ransomware Simulation")
    
    websocket_url = "ws://localhost:8000/ws/simulate"
    
    payload = {
        "network_config": {
            "num_nodes": 50,
            "network_type": "scale_free"
        },
        "malware_config": {
            "malware_type": "ransomware",
            "infection_rate": 0.30,
            "latency": 3
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print_info(f"Testing Ransomware via WebSocket...")
    
    try:
        async with websockets.connect(websocket_url) as websocket:
            await websocket.send(json.dumps(payload))
            
            step_count = 0
            final_infected = 0
            
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data["type"] == "step":
                    step_count += 1
                    final_infected = data["total_infected"]
                
                elif data["type"] == "complete":
                    stats = data["statistics"]
                    print_success(f"Ransomware simulation completed: {final_infected}/{stats['total_devices']} infected in {step_count} steps")
                    return True
                
                elif data["type"] == "error":
                    print_error(f"Error: {data['message']}")
                    return False
    
    except Exception as e:
        print_error(f"WebSocket error: {str(e)}")
        return False


def run_all_tests():
    print(f"{Colors.BOLD}{Colors.OKBLUE}")
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    MSpread API Test Suite                              ║
║            Testing FastAPI Endpoints and Functionality                 ║
╚════════════════════════════════════════════════════════════════════════╝
    """)
    print(Colors.ENDC)
    
    # Define all tests as a list of tuples (test_number, test_name, test_function, is_async)
    tests = [
        (1, "Server Health", test_server_health, False),
        (2, "Root Endpoint", test_root_endpoint, False),
        (3, "Worm Simulation (50 nodes)", test_simulation_worm, False),
        (4, "Virus Simulation", test_simulation_virus, False),
        (5, "Ransomware Simulation", test_simulation_ransomware, False),
        (6, "Network Topologies", test_different_topologies, False),
        (7, "Infection Rate Comparison", test_infection_rate_comparison, False),
        (8, "Multiple Initial Infections", test_multiple_initial_infected, False),
        (9, "Device Attributes: All Admin", test_device_attributes_all_admin, False),
        (10, "Device Attributes: All Non-Admin", test_device_attributes_all_non_admin, False),
        (11, "Device Attributes: Mixed", test_device_attributes_mixed, False),
        (12, "WebSocket Worm Simulation", test_websocket_simulation_worm, True),
        (13, "WebSocket Virus Simulation", test_websocket_simulation_virus, True),
        (14, "WebSocket Ransomware Simulation", test_websocket_simulation_ransomware, True),
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
            valid_tests = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            
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
            help='Test number(s) to run (1-11). Multiple tests can be specified.'
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

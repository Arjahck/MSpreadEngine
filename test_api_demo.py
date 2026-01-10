"""
Test suite for MSpread API endpoints.

This script tests the FastAPI server by making HTTP requests to all available endpoints.
Make sure the API server is running before executing this script:
    python main.py run

Run this test file with:
    python test_api_demo.py
"""

import requests
import json
import time
from typing import Dict, List
import sys

# API server configuration
API_BASE_URL = "http://localhost:8000"
API_VERSION = "/api/v1"

# Colors for terminal output
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
    """Print a formatted header."""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"{text:^70}")
    print(f"{'='*70}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message."""
    print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message."""
    print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")


def test_server_health() -> bool:
    """Test if the API server is running and healthy."""
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
    """Test the root endpoint."""
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
    """Test worm malware simulation."""
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
    """Test virus malware simulation."""
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
    """Test ransomware malware simulation."""
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
    """Test simulations with different network topologies."""
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
    """Test how different infection rates affect spread."""
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


def run_all_tests():
    """Run all API tests."""
    print(f"{Colors.BOLD}{Colors.OKBLUE}")
    print("""
╔════════════════════════════════════════════════════════════════════════╗
║                    MSpread API Test Suite                              ║
║            Testing FastAPI Endpoints and Functionality                 ║
╚════════════════════════════════════════════════════════════════════════╝
    """)
    print(Colors.ENDC)
    
    results = {}
    
    # Test 1: Server Health
    results["Server Health"] = test_server_health()
    if not results["Server Health"]:
        print_error("\nCannot connect to API server. Aborting tests.")
        return
    
    # Test 2: Root Endpoint
    results["Root Endpoint"] = test_root_endpoint()
    
    # Test 3: Worm Simulation (small network)
    results["Worm Simulation (50 nodes)"] = test_simulation_worm(50)
    
    # Test 4: Virus Simulation
    results["Virus Simulation"] = test_simulation_virus(50)
    
    # Test 5: Ransomware Simulation
    results["Ransomware Simulation"] = test_simulation_ransomware(50)
    
    # Test 6: Different Topologies
    results["Network Topologies"] = test_different_topologies()
    
    # Test 7: Infection Rate Comparison
    results["Infection Rate Comparison"] = test_infection_rate_comparison()
    
    # Test 8: Multiple Initial Infections
    results["Multiple Initial Infections"] = test_multiple_initial_infected()
    
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


if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Tests interrupted by user{Colors.ENDC}")
        sys.exit(1)

#!/usr/bin/env python
"""
Example: Using Node Definitions for Network Segmentation

This script demonstrates how to use node definitions and batch logic
to create realistic network simulations with device segmentation.

Requirements:
    - MSpreadEngine API server running (python main.py run)
    - requests library (pip install requests)

Usage:
    python example_node_definitions.py
"""

import requests
import json
from typing import Dict, List

API_BASE_URL = "http://localhost:8000"
API_VERSION = "/api/v1"


def print_result(title: str, result: Dict):
    """Pretty print simulation results."""
    print(f"\n{'='*70}")
    print(f"{title:^70}")
    print(f"{'='*70}")
    print(f"Total Devices:        {result['total_devices']}")
    print(f"Total Infected:       {result['total_infected']}")
    print(f"Infection Rate:       {result['infection_percentage']:.2f}%")
    print(f"Simulation Steps:     {result['total_steps']}")
    print(f"Malware Type:         {result['malware_type']}")
    print(f"{'='*70}\n")


def example_1_simple_split():
    """Example 1: Simple 70/30 admin/non-admin split."""
    print("\n" + "="*70)
    print("Example 1: Simple 70/30 Admin/Non-Admin Split")
    print("="*70)
    print("\nScenario:")
    print("  - 100 network devices")
    print("  - 70 admin users (servers)")
    print("  - 30 non-admin users (workstations)")
    print("  - Worm infection starting on device_0 (admin)")
    
    payload = {
        "network_config": {
            "num_nodes": 100,
            "network_type": "scale_free",
            "node_definitions": [
                {"count": 70, "attributes": {"admin_user": True, "device_type": "server"}},
                {"count": 30, "attributes": {"admin_user": False, "device_type": "workstation"}}
            ]
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    print("\nSending simulation request...")
    response = requests.post(
        f"{API_BASE_URL}{API_VERSION}/simulate",
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print_result("Simulation Results: 70/30 Split", result)
        print("Interpretation:")
        print(f"  - Infection spread to {result['total_infected']} devices")
        print(f"  - Privilege boundary limited spread effectiveness")
        return True
    else:
        print(f"ERROR: Simulation failed with status {response.status_code}")
        return False


def example_2_three_tier_network():
    """Example 2: Enterprise three-tier network segmentation."""
    print("\n" + "="*70)
    print("Example 2: Enterprise Three-Tier Network Segmentation")
    print("="*70)
    print("\nScenario:")
    print("  - 200 total devices across three tiers")
    print("  - Tier 1: 20 critical servers (fully secured)")
    print("  - Tier 2: 100 admin workstations (secured)")
    print("  - Tier 3: 80 guest workstations (minimal security)")
    
    payload = {
        "network_config": {
            "num_nodes": 200,
            "network_type": "scale_free",
            "node_definitions": [
                {
                    "count": 20,
                    "attributes": {
                        "admin_user": True,
                        "device_type": "server",
                        "firewall_enabled": True,
                        "antivirus": True,
                        "patch_status": "fully_patched"
                    }
                },
                {
                    "count": 100,
                    "attributes": {
                        "admin_user": True,
                        "device_type": "workstation",
                        "firewall_enabled": True,
                        "antivirus": True,
                        "patch_status": "patched"
                    }
                },
                {
                    "count": 80,
                    "attributes": {
                        "admin_user": False,
                        "device_type": "workstation",
                        "firewall_enabled": False,
                        "antivirus": False,
                        "patch_status": "unpatched"
                    }
                }
            ]
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_150"],  # Start in guest tier (non-admin)
        "max_steps": 50
    }
    
    print("\nSending simulation request...")
    print("  - Malware starting on guest workstation (device_150)")
    response = requests.post(
        f"{API_BASE_URL}{API_VERSION}/simulate",
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print_result("Simulation Results: Three-Tier Network", result)
        print("Interpretation:")
        print(f"  - Guest tier devices: All {result['total_infected']} can be infected")
        print(f"  - Admin tiers protected by privilege boundary")
        print(f"  - Non-admin malware cannot breach to admin devices")
        return True
    else:
        print(f"ERROR: Simulation failed with status {response.status_code}")
        return False


def example_3_mixed_operating_systems():
    """Example 3: Network with mixed operating systems."""
    print("\n" + "="*70)
    print("Example 3: Network with Mixed Operating Systems")
    print("="*70)
    print("\nScenario:")
    print("  - 150 total devices")
    print("  - 50 Windows servers (high security)")
    print("  - 50 Linux workstations (moderate security)")
    print("  - 50 Mixed guest devices (low security)")
    
    payload = {
        "network_config": {
            "num_nodes": 150,
            "network_type": "scale_free",
            "device_attributes": {"firewall_enabled": True},  # All have firewalls
            "node_definitions": [
                {
                    "count": 50,
                    "attributes": {
                        "admin_user": True,
                        "os": "Windows Server 2019",
                        "device_type": "server",
                        "antivirus": True
                    }
                },
                {
                    "count": 50,
                    "attributes": {
                        "admin_user": True,
                        "os": "Linux Ubuntu 20.04",
                        "device_type": "workstation",
                        "antivirus": False
                    }
                },
                {
                    "count": 50,
                    "attributes": {
                        "admin_user": False,
                        "os": "Windows 10",
                        "device_type": "workstation",
                        "antivirus": False
                    }
                }
            ]
        },
        "malware_config": {
            "malware_type": "virus",
            "infection_rate": 0.25,
            "latency": 2
        },
        "initial_infected": ["device_0"],  # Start on Windows server
        "max_steps": 50
    }
    
    print("\nSending simulation request...")
    print("  - Virus starting on Windows server (device_0)")
    print("  - All devices have firewalls enabled (network-wide)")
    response = requests.post(
        f"{API_BASE_URL}{API_VERSION}/simulate",
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print_result("Simulation Results: Mixed OS Network", result)
        print("Interpretation:")
        print(f"  - {result['total_infected']} devices infected across all tiers")
        print(f"  - OS diversity: Windows, Linux, mixed environments")
        print(f"  - Firewall: Present on all devices (defense mechanism)")
        return True
    else:
        print(f"ERROR: Simulation failed with status {response.status_code}")
        return False


def example_4_progressive_hardening():
    """Example 4: Network with progressive security hardening."""
    print("\n" + "="*70)
    print("Example 4: Network with Progressive Security Hardening")
    print("="*70)
    print("\nScenario:")
    print("  - 120 total devices")
    print("  - Batch 1: 40 unprotected devices")
    print("  - Batch 2: 40 basic protection (antivirus only)")
    print("  - Batch 3: 40 full protection (firewall + antivirus + admin)")
    
    payload = {
        "network_config": {
            "num_nodes": 120,
            "network_type": "scale_free",
            "node_definitions": [
                {
                    "count": 40,
                    "attributes": {
                        "admin_user": False,
                        "firewall_enabled": False,
                        "antivirus": False,
                        "patch_status": "unpatched"
                    }
                },
                {
                    "count": 40,
                    "attributes": {
                        "admin_user": False,
                        "firewall_enabled": False,
                        "antivirus": True,
                        "patch_status": "patched"
                    }
                },
                {
                    "count": 40,
                    "attributes": {
                        "admin_user": True,
                        "firewall_enabled": True,
                        "antivirus": True,
                        "patch_status": "fully_patched"
                    }
                }
            ]
        },
        "malware_config": {
            "malware_type": "ransomware",
            "infection_rate": 0.30,
            "latency": 3
        },
        "initial_infected": ["device_10"],  # Start in unprotected batch
        "max_steps": 50
    }
    
    print("\nSending simulation request...")
    print("  - Ransomware starting in unprotected batch")
    response = requests.post(
        f"{API_BASE_URL}{API_VERSION}/simulate",
        json=payload,
        timeout=60
    )
    
    if response.status_code == 200:
        result = response.json()
        print_result("Simulation Results: Progressive Hardening", result)
        print("Interpretation:")
        print(f"  - Infection rate: {result['infection_percentage']:.1f}%")
        print(f"  - Demonstrates impact of layered defenses")
        print(f"  - Admin tier uses privilege boundary (admin_user=True)")
        return True
    else:
        print(f"ERROR: Simulation failed with status {response.status_code}")
        return False


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("MSpreadEngine: Node Definitions & Batch Logic Examples")
    print("="*70)
    print("\nMake sure the API server is running:")
    print("  python main.py run")
    
    results = []
    
    # Run examples
    results.append(("Example 1: Simple 70/30 Split", example_1_simple_split()))
    results.append(("Example 2: Three-Tier Network", example_2_three_tier_network()))
    results.append(("Example 3: Mixed OS Network", example_3_mixed_operating_systems()))
    results.append(("Example 4: Progressive Hardening", example_4_progressive_hardening()))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    for name, success in results:
        status = "✓ PASSED" if success else "✗ FAILED"
        print(f"{name:40} {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} examples completed successfully")
    
    print("\n" + "="*70)
    print("Key Takeaways:")
    print("="*70)
    print("""
1. Node definitions enable flexible network segmentation
2. Batches are applied sequentially in device_0 to device_n order
3. admin_user attribute controls privilege boundaries in spread logic
4. Multiple attributes per batch provide realistic scenarios
5. Works with any malware type (worm, virus, ransomware)
6. Compatible with all network topologies (scale_free, small_world, etc.)
7. Useful for simulating enterprise, educational, and IoT networks
    """)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to API server at http://localhost:8000")
        print("Make sure the API server is running:")
        print("  python main.py run")

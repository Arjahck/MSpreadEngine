#!/usr/bin/env python
"""
Quick test to show the new device attribute tests are available
"""

import sys
sys.path.insert(0, '.')

# Import test functions
from test_api_demo import (
    test_device_attributes_all_admin,
    test_device_attributes_all_non_admin,
    test_device_attributes_mixed
)

print("✓ Successfully imported new device attribute tests:\n")
print("  - test_device_attributes_all_admin()")
print("  - test_device_attributes_all_non_admin()")
print("  - test_device_attributes_mixed()\n")

print("Available test numbers in test_api_demo.py:")
print("  1. Server Health")
print("  2. Root Endpoint")
print("  3. Worm Simulation (50 nodes)")
print("  4. Virus Simulation")
print("  5. Ransomware Simulation")
print("  6. Network Topologies")
print("  7. Infection Rate Comparison")
print("  8. Multiple Initial Infections")
print("  9. Device Attributes: All Admin")
print("  10. Device Attributes: All Non-Admin")
print("  11. Device Attributes: Mixed")
print("  12. WebSocket Worm Simulation")
print("  13. WebSocket Virus Simulation")
print("  14. WebSocket Ransomware Simulation\n")

print("Usage Examples:")
print("  python test_api_demo.py              # Run all tests")
print("  python test_api_demo.py -t 9         # Run test 9 (All Admin)")
print("  python test_api_demo.py -t 10        # Run test 10 (All Non-Admin)")
print("  python test_api_demo.py -t 11        # Run test 11 (Mixed)")
print("  python test_api_demo.py -t 9 10 11   # Run all device attribute tests\n")

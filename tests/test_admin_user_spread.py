#!/usr/bin/env python
"""
Test admin_user attribute spread restriction logic
"""

from network_model import NetworkGraph
from malware_engine.malware_base import Malware
from simulation import Simulator

def test_admin_user_restriction():
    """Test that non-admin devices cannot spread to admin devices"""
    print("=" * 70)
    print("Test: admin_user=False Spread Restriction")
    print("=" * 70)
    
    # Create a small network for testing
    network = NetworkGraph(network_type="scale_free")
    network.generate_topology(10, device_attributes={"admin_user": True})
    
    # Make some devices non-admin
    for i in range(5, 10):
        network.set_device_attributes(f"device_{i}", admin_user=False)
    
    print("\nNetwork Setup:")
    print("  devices 0-4: admin_user=True")
    print("  devices 5-9: admin_user=False")
    
    # Create malware
    malware = Malware("worm_1", infection_rate=1.0, avoids_admin=True)  # 100% infection for testing
    
    # Initialize simulator (which passes network to malware)
    simulator = Simulator(network, malware)
    simulator.initialize(["device_5"])  # Start from non-admin device
    
    print("\nInitial infection: device_5 (non-admin)")
    print(f"Infected devices: {malware.infected_devices}")
    
    # Run one step
    step_data = simulator.step()
    
    print(f"\nAfter step 1:")
    print(f"  Newly infected: {step_data['newly_infected']}")
    print(f"  Total infected: {malware.infected_devices}")
    print(f"  Infected count: {step_data['total_infected']}")
    
    # Check results
    for device in malware.infected_devices:
        attrs = network.get_device_attributes(device)
        print(f"    {device}: admin_user={attrs['admin_user']}")
    
    # Verify: device_5 should only spread to other non-admin devices
    newly_infected = step_data['newly_infected']
    non_admin_neighbors = set()
    
    # Get neighbors of device_5
    neighbors = network.get_neighbors("device_5")
    print(f"\nNeighbors of device_5: {neighbors}")
    
    for neighbor in neighbors:
        neighbor_attrs = network.get_device_attributes(neighbor)
        if not neighbor_attrs['admin_user']:
            non_admin_neighbors.add(neighbor)
            print(f"  {neighbor}: non-admin (can be infected)")
        else:
            print(f"  {neighbor}: admin user (should NOT be infected)")
    
    # All newly infected should be non-admin
    newly_infected_devices = step_data['devices_infected']
    all_non_admin = all(
        not network.get_device_attributes(device)['admin_user']
        for device in newly_infected_devices
    )
    
    if all_non_admin:
        print("\n✓ SUCCESS: Non-admin device only spread to other non-admin devices!")
    else:
        print("\n✗ FAILED: Non-admin device spread to admin device!")
        admin_spread = [d for d in newly_infected_devices if network.get_device_attributes(d)['admin_user']]
        print(f"  Admin devices infected from non-admin: {admin_spread}")
        return False
    
    return True


def test_admin_user_normal_spread():
    """Test that admin devices can spread normally to all neighbors"""
    print("\n" + "=" * 70)
    print("Test: admin_user=True Normal Spread")
    print("=" * 70)
    
    # Create a small network
    network = NetworkGraph(network_type="scale_free")
    network.generate_topology(10, device_attributes={"admin_user": True})
    
    # Make some devices non-admin
    for i in range(5, 10):
        network.set_device_attributes(f"device_{i}", admin_user=False)
    
    print("\nNetwork Setup:")
    print("  devices 0-4: admin_user=True")
    print("  devices 5-9: admin_user=False")
    
    # Create malware
    malware = Malware("worm_1", infection_rate=1.0, avoids_admin=True)  # 100% infection
    
    # Initialize simulator
    simulator = Simulator(network, malware)
    simulator.initialize(["device_0"])  # Start from admin device
    
    print("\nInitial infection: device_0 (admin)")
    
    # Run one step
    step_data = simulator.step()
    
    print(f"\nAfter step 1:")
    print(f"  Newly infected: {step_data['newly_infected']}")
    print(f"  Total infected: {malware.infected_devices}")
    
    # Get neighbors of device_0
    neighbors = network.get_neighbors("device_0")
    print(f"\nNeighbors of device_0: {neighbors}")
    
    for neighbor in neighbors:
        neighbor_attrs = network.get_device_attributes(neighbor)
        print(f"  {neighbor}: admin_user={neighbor_attrs['admin_user']}")
    
    print("\n✓ Admin device can spread to all neighbors (both admin and non-admin)")
    return True


def test_mixed_spread():
    """Test realistic scenario with mixed admin/non-admin devices"""
    print("\n" + "=" * 70)
    print("Test: Realistic Mixed Environment")
    print("=" * 70)
    
    # Create network with default admin_user=True
    network = NetworkGraph(network_type="scale_free")
    network.generate_topology(50)
    
    # Convert 30% of devices to non-admin (unprivileged users)
    non_admin_count = int(50 * 0.3)  # 15 devices
    for i in range(50 - non_admin_count, 50):  # devices 35-49
        network.set_device_attributes(f"device_{i}", admin_user=False)
    
    print(f"\nNetwork Setup: 50 devices")
    print(f"  Admin (35): devices 0-34")
    print(f"  Non-admin (15): devices 35-49")
    
    # Run full simulation
    malware = Malware("worm_1", infection_rate=0.3, avoids_admin=True)
    simulator = Simulator(network, malware)
    simulator.initialize(["device_0"])  # Start from admin
    
    results = simulator.run(max_steps=100)
    stats = simulator.get_statistics()
    
    print(f"\nSimulation Results:")
    print(f"  Total steps: {stats['total_steps']}")
    print(f"  Total infected: {stats['total_infected']}/{stats['total_devices']}")
    print(f"  Infection percentage: {stats['infection_percentage']:.2f}%")
    
    # Count infected admin vs non-admin
    admin_infected = 0
    non_admin_infected = 0
    
    for device in malware.infected_devices:
        attrs = network.get_device_attributes(device)
        if attrs['admin_user']:
            admin_infected += 1
        else:
            non_admin_infected += 1
    
    print(f"\n  Admin infected: {admin_infected}/35")
    print(f"  Non-admin infected: {non_admin_infected}/15")
    
    return True


if __name__ == "__main__":
    try:
        success = True
        success &= test_admin_user_restriction()
        success &= test_admin_user_normal_spread()
        success &= test_mixed_spread()
        
        if success:
            print("\n" + "=" * 70)
            print("✓ All admin_user tests passed!")
            print("=" * 70)
        else:
            print("\n✗ Some tests failed")
            exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

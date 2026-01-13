#!/usr/bin/env python
"""
Test device attributes functionality
"""

from network_model import NetworkGraph

def test_default_attributes():
    """Test that default attributes are applied correctly"""
    print("Test 1 - Default attributes...")
    net = NetworkGraph()
    net.generate_topology(10)
    attrs = net.get_device_attributes('device_0')
    
    assert attrs.get('admin_user') == True, "Default admin_user should be True"
    assert attrs.get('device_type') == 'workstation', "Default device_type should be workstation"
    assert attrs.get('os') is None, "Default os should be None"
    print("  ✓ Default attributes correct")

def test_custom_attributes():
    """Test that custom attributes override defaults"""
    print("Test 2 - Custom attributes...")
    net = NetworkGraph()
    net.generate_topology(10, device_attributes={
        'os': 'Windows Server 2019',
        'patch_status': 'patched',
        'firewall_enabled': True,
        'admin_user': False
    })
    attrs = net.get_device_attributes('device_0')
    
    assert attrs.get('os') == 'Windows Server 2019', "os should be Windows Server 2019"
    assert attrs.get('patch_status') == 'patched', "patch_status should be patched"
    assert attrs.get('firewall_enabled') == True, "firewall_enabled should be True"
    assert attrs.get('admin_user') == False, "admin_user should be False"
    print("  ✓ Custom attributes applied correctly")

def test_modify_attributes():
    """Test that attributes can be modified after creation"""
    print("Test 3 - Modify attributes...")
    net = NetworkGraph()
    net.generate_topology(10)
    
    # Modify device_1
    net.set_device_attributes('device_1', os='Ubuntu 20.04', admin_user=False)
    attrs = net.get_device_attributes('device_1')
    
    assert attrs.get('os') == 'Ubuntu 20.04', "os should be Ubuntu 20.04"
    assert attrs.get('admin_user') == False, "admin_user should be False"
    
    # Verify device_0 is unchanged
    attrs0 = net.get_device_attributes('device_0')
    assert attrs0.get('os') is None, "device_0 os should still be None"
    assert attrs0.get('admin_user') == True, "device_0 admin_user should still be True"
    
    print("  ✓ Attributes modified correctly")

def test_attribute_consistency():
    """Test that all nodes have the same custom attributes"""
    print("Test 4 - Attribute consistency across nodes...")
    net = NetworkGraph()
    net.generate_topology(50, device_attributes={
        'device_type': 'server',
        'os': 'Windows Server 2019',
        'antivirus': True
    })
    
    for i in range(5):
        attrs = net.get_device_attributes(f'device_{i}')
        assert attrs.get('device_type') == 'server', f"device_{i} should be server type"
        assert attrs.get('os') == 'Windows Server 2019', f"device_{i} should have Windows Server 2019"
        assert attrs.get('antivirus') == True, f"device_{i} should have antivirus"
    
    print("  ✓ All nodes have consistent attributes")

if __name__ == "__main__":
    try:
        test_default_attributes()
        test_custom_attributes()
        test_modify_attributes()
        test_attribute_consistency()
        print("\n✓ All device attribute tests passed!")
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        exit(1)

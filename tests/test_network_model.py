"""Unit tests for network model."""

import unittest
from network_model import NetworkGraph


class TestNetworkGraph(unittest.TestCase):
    """Test cases for NetworkGraph class."""

    def setUp(self):
        """Set up test fixtures."""
        self.network = NetworkGraph(network_type="scale_free")

    def test_add_device(self):
        """Test adding a device to the network."""
        self.network.add_device("device_1", device_type="workstation")
        self.assertIn("device_1", self.network.graph.nodes())

    def test_add_connection(self):
        """Test adding a connection between devices."""
        self.network.add_device("device_1")
        self.network.add_device("device_2")
        self.network.add_connection("device_1", "device_2")
        self.assertTrue(self.network.graph.has_edge("device_1", "device_2"))

    def test_generate_topology(self):
        """Test generating a network topology."""
        self.network.generate_topology(num_nodes=10)
        self.assertEqual(self.network.graph.number_of_nodes(), 10)

    def test_get_neighbors(self):
        """Test getting neighbors of a device."""
        self.network.add_device("device_1")
        self.network.add_device("device_2")
        self.network.add_device("device_3")
        self.network.add_connection("device_1", "device_2")
        self.network.add_connection("device_1", "device_3")
        
        neighbors = self.network.get_neighbors("device_1")
        self.assertEqual(len(neighbors), 2)
        self.assertIn("device_2", neighbors)
        self.assertIn("device_3", neighbors)


if __name__ == "__main__":
    unittest.main()

"""
Network graph representation using NetworkX.

This module provides graph-based network representation for modeling
devices and their connections.
"""

import networkx as nx
from typing import List, Dict, Tuple, Optional
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logger = logging.getLogger(__name__)

try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    logger.warning("tqdm not installed. Install with: pip install tqdm for progress bars")


class NetworkGraph:

    # Default device attributes
    DEFAULT_DEVICE_ATTRIBUTES = {
        "os": None,
        "patch_status": None,
        "device_type": "workstation",
        "firewall_enabled": None,
        "antivirus": None,
        "admin_user": True, 
    }

    def __init__(self, network_type: str = "scale_free"):
        self.graph = nx.Graph()
        self.network_type = network_type
        self.device_states = {}  # Track device infection states

    def add_device(self, device_id: str, **attributes) -> None:
        """ Add a device node with optional attributes. """
        device_attrs = self.DEFAULT_DEVICE_ATTRIBUTES.copy()
        device_attrs.update(attributes)
        
        self.graph.add_node(device_id, **device_attrs)
        self.device_states[device_id] = "healthy"

    def set_device_attributes(self, device_id: str, **attributes) -> None:
        if device_id not in self.graph.nodes():
            raise ValueError(f"Device {device_id} not found in network")
        
        for key, value in attributes.items():
            self.graph.nodes[device_id][key] = value

    def get_device_attributes(self, device_id: str) -> Dict:

        if device_id not in self.graph.nodes():
            raise ValueError(f"Device {device_id} not found in network")
        
        return dict(self.graph.nodes[device_id])

    def add_connection(self, device1: str, device2: str, connection_type: str = "network", **attributes) -> None:
        """
        Add a connection between two devices.

        Args:
            device1: First device ID
            device2: Second device ID
            connection_type: Type of connection (network, direct, wireless, etc.)
            **attributes: Additional connection attributes (bandwidth, latency, etc.)
        """
        self.graph.add_edge(device1, device2, connection_type=connection_type, **attributes)

    def generate_topology(self, num_nodes: int, use_parallel: bool = True, num_workers: int = 8, device_attributes: Optional[Dict] = None, **kwargs) -> None:
        """
        Generate a network topology based on the specified type.
        
        Args:
            num_nodes: Number of nodes in the network
            use_parallel: Use parallel processing for node creation (default: True)
            num_workers: Number of worker threads (default: 8, adjust based on CPU cores)
            device_attributes: Dictionary of default device attributes to apply to all nodes
                              (e.g., {"os": "Windows Server 2019", "patch_status": "patched", ...})
            **kwargs: Additional parameters for topology generation
        """
        import time
        start_time = time.time()
        
        logger.info(f"Generating {num_nodes}-node {self.network_type} topology...")
        
        if self.network_type == "scale_free":
            logger.info("Creating Barabasi-Albert scale-free graph...")
            base_graph = nx.barabasi_albert_graph(num_nodes, 3)
        elif self.network_type == "small_world":
            logger.info("Creating Watts-Strogatz small-world graph...")
            base_graph = nx.watts_strogatz_graph(num_nodes, 4, 0.3)
        elif self.network_type == "random":
            logger.info("Creating Erdos-Renyi random graph...")
            base_graph = nx.erdos_renyi_graph(num_nodes, 0.1)
        elif self.network_type == "complete":
            logger.info("Creating complete graph...")
            base_graph = nx.complete_graph(num_nodes)
        else:
            raise ValueError(f"Unknown network type: {self.network_type}")

        logger.info("Adding nodes to graph...")
        
        base_attrs = self.DEFAULT_DEVICE_ATTRIBUTES.copy()
        if device_attributes:
            base_attrs.update(device_attributes)
        
        node_list = [(f"device_{node}", base_attrs.copy()) for node in base_graph.nodes()]
        
        if HAS_TQDM:
            node_list_iter = tqdm(node_list, desc="Adding nodes", unit="nodes", disable=len(node_list) < 1000)
        else:
            node_list_iter = node_list
            
        if use_parallel and num_nodes > 1000:
            batch_size = max(1000, num_nodes // num_workers)
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                for i in range(0, len(node_list), batch_size):
                    batch = node_list[i:i+batch_size]
                    future = executor.submit(self._add_nodes_batch, batch)
                    futures.append(future)
                
                for future in as_completed(futures):
                    future.result()
        else:
            for node_id, attrs in node_list_iter:
                self.graph.add_node(node_id, **attrs)
                self.device_states[node_id] = "healthy"

        logger.info("Adding edges to graph...")
        edge_list = [(f"device_{u}", f"device_{v}") for u, v in base_graph.edges()]
        
        if HAS_TQDM:
            edge_list_iter = tqdm(edge_list, desc="Adding edges", unit="edges", disable=len(edge_list) < 10000)
        else:
            edge_list_iter = edge_list
            
        if use_parallel and len(edge_list) > 10000:
            batch_size = max(5000, len(edge_list) // num_workers)
            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = []
                for i in range(0, len(edge_list), batch_size):
                    batch = edge_list[i:i+batch_size]
                    future = executor.submit(self._add_edges_batch, batch)
                    futures.append(future)
                
                for future in as_completed(futures):
                    future.result()
        else:
            for device1, device2 in edge_list_iter:
                self.graph.add_edge(device1, device2, connection_type="network")

        elapsed_time = time.time() - start_time
        logger.info(f"Topology generated in {elapsed_time:.2f}s")
        logger.info(f"  Nodes: {self.graph.number_of_nodes()}")
        logger.info(f"  Edges: {self.graph.number_of_edges()}")

    def _add_nodes_batch(self, node_list: List[Tuple[str, Dict]]) -> None:
        for node_id, attrs in node_list:
            self.graph.add_node(node_id, **attrs)
            self.device_states[node_id] = "healthy"

    def _add_edges_batch(self, edge_list: List[Tuple[str, str]]) -> None:
        for device1, device2 in edge_list:
            self.graph.add_edge(device1, device2, connection_type="network")

    def get_neighbors(self, device_id: str) -> List[str]:
        return list(self.graph.neighbors(device_id))

    def get_device_info(self, device_id: str) -> Optional[Dict]:
        if device_id in self.graph:
            return dict(self.graph.nodes[device_id])
        return None

    def to_json(self, filepath: str) -> None:
        data = {
            "nodes": [{"id": node, **self.graph.nodes[node]} for node in self.graph.nodes()],
            "edges": [
                {
                    "source": u,
                    "target": v,
                    **self.graph[u][v]
                }
                for u, v in self.graph.edges()
            ],
            "network_type": self.network_type,
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def from_json(self, filepath: str) -> None:
        with open(filepath, "r") as f:
            data = json.load(f)

        self.network_type = data.get("network_type", "unknown")
        self.graph.clear()

        for node_data in data.get("nodes", []):
            node_id = node_data.pop("id")
            self.add_device(node_id, **node_data)

        for edge_data in data.get("edges", []):
            source = edge_data.pop("source")
            target = edge_data.pop("target")
            self.add_connection(source, target, **edge_data)

    def get_statistics(self, skip_expensive: bool = False) -> Dict:
        """Get network statistics including structural metrics and attribute demographics."""
        stats = {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
        }
        
        # Attribute Demographics (OS and Admin ratio)
        os_counts = {}
        admin_count = 0
        for n in self.graph.nodes:
            attrs = self.graph.nodes[n]
            os = attrs.get('os', 'Unknown')
            os_counts[str(os)] = os_counts.get(str(os), 0) + 1
            if attrs.get('admin_user'):
                admin_count += 1
        
        stats["demographics"] = {
            "os_breakdown": os_counts,
            "admin_ratio": admin_count / stats["num_nodes"] if stats["num_nodes"] > 0 else 0
        }

        # Degree Statistics
        degrees = [d for n, d in self.graph.degree()]
        if degrees:
            stats["avg_degree"] = sum(degrees) / len(degrees)
            stats["max_degree"] = max(degrees)
        else:
            stats["avg_degree"] = 0
            stats["max_degree"] = 0
        
        if not skip_expensive:
            # Component Analysis
            components = list(nx.connected_components(self.graph))
            stats["num_components"] = len(components)
            stats["giant_component_size"] = len(max(components, key=len)) if components else 0

            logger.info("Computing clustering coefficient...")
            stats["avg_clustering"] = nx.average_clustering(self.graph)
            
            # Assortativity (Hub-to-hub connectivity)
            try:
                stats["assortativity"] = nx.degree_assortativity_coefficient(self.graph)
            except Exception:
                stats["assortativity"] = None

            if nx.is_connected(self.graph):
                logger.info("Computing diameter...")
                stats["diameter"] = nx.diameter(self.graph)
            else:
                stats["diameter"] = None
        else:
            stats.update({
                "num_components": None,
                "giant_component_size": None,
                "avg_clustering": None,
                "assortativity": None,
                "diameter": None
            })
            
        return stats

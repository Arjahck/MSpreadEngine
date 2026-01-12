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

    def __init__(self, network_type: str = "scale_free"):
        self.graph = nx.Graph()
        self.network_type = network_type
        self.device_states = {}  # Track device infection states

    def add_device(self, device_id: str, device_type: str = "workstation", **attributes) -> None:
        """
        Args:
            device_id: Unique identifier for the device
            device_type: Type of device (workstation, server, router, etc.)
            **attributes: Additional device attributes
        """
        self.graph.add_node(device_id, device_type=device_type, **attributes)
        self.device_states[device_id] = "healthy"

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

    def generate_topology(self, num_nodes: int, use_parallel: bool = True, num_workers: int = 8, **kwargs) -> None:
        """
        Generate a network topology based on the specified type.
        
        Optimized for large networks with multi-threaded node/edge creation.

        Args:
            num_nodes: Number of nodes in the network
            use_parallel: Use parallel processing for node creation (default: True)
            num_workers: Number of worker threads (default: 8, adjust based on CPU cores)
            **kwargs: Additional parameters for topology generation
        """
        import time
        start_time = time.time()
        
        logger.info(f"Generating {num_nodes}-node {self.network_type} topology...")
        
        # Generate base graph
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

        # Optimized: Add all nodes at once using add_nodes_from for better performance
        logger.info("Adding nodes to graph...")
        node_list = [(f"device_{node}", {"device_type": "workstation"}) for node in base_graph.nodes()]
        
        if HAS_TQDM:
            node_list_iter = tqdm(node_list, desc="Adding nodes", unit="nodes", disable=len(node_list) < 1000)
        else:
            node_list_iter = node_list
            
        if use_parallel and num_nodes > 1000:
            # Multi-threaded for better performance
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
            # Single-threaded for smaller networks
            for node_id, attrs in node_list_iter:
                self.graph.add_node(node_id, **attrs)
                self.device_states[node_id] = "healthy"

        # Optimized: Add edges efficiently
        logger.info("Adding edges to graph...")
        edge_list = [(f"device_{u}", f"device_{v}") for u, v in base_graph.edges()]
        
        if HAS_TQDM:
            edge_list_iter = tqdm(edge_list, desc="Adding edges", unit="edges", disable=len(edge_list) < 10000)
        else:
            edge_list_iter = edge_list
            
        if use_parallel and len(edge_list) > 10000:
            # Multi-threaded for better performance
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
            # Single-threaded for smaller networks
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

        # Add nodes
        for node_data in data.get("nodes", []):
            node_id = node_data.pop("id")
            self.add_device(node_id, **node_data)

        # Add edges
        for edge_data in data.get("edges", []):
            source = edge_data.pop("source")
            target = edge_data.pop("target")
            self.add_connection(source, target, **edge_data)

    def get_statistics(self, skip_expensive: bool = False) -> Dict:
        """
        Get network statistics.
        
        For very large networks, skip_expensive=True will avoid expensive calculations
        like diameter and average clustering (which scale as O(n²) or worse).

        Args:
            skip_expensive: Skip expensive calculations (default: False)

        Returns:
            Dictionary with network statistics
        """
        stats = {
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
        }
        
        if not skip_expensive:
            logger.info("Computing clustering coefficient (this may take time for large graphs)...")
            stats["avg_clustering"] = nx.average_clustering(self.graph)
            
            if nx.is_connected(self.graph):
                logger.info("Computing diameter (this may take time for large graphs)...")
                stats["diameter"] = nx.diameter(self.graph)
            else:
                stats["diameter"] = None
        else:
            stats["avg_clustering"] = None
            stats["diameter"] = None
            
        return stats

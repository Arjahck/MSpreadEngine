"""Network model module for MSpread."""

try:
    from .network_graph import NetworkGraph
except ImportError:
    from network_graph import NetworkGraph

__all__ = ["NetworkGraph"]

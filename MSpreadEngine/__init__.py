"""
MSpread: Malware Spreading Simulation and Visualization Tool

A comprehensive framework for modeling and visualizing malware propagation
across networks ranging from large corporate environments to country-wide
infrastructures using NetworkX.
"""

__version__ = "0.1.0"
__author__ = "Arjahck"
__description__ = "Malware Spreading Simulation and Visualization Tool"

from .network_model import NetworkGraph
from .malware_engine import Malware
from .simulation import Simulator

__all__ = [
    "NetworkGraph",
    "Malware",
    "Simulator",
]

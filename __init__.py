"""
MSpreadEngine: Malware Spreading Simulation Engine

A comprehensive framework for modeling and simulating malware propagation
across networks ranging from small corporate environments to country-wide
infrastructures using NetworkX.
"""

__version__ = "0.1.8"
__author__ = "Arjahck"
__description__ = "Malware Spreading Simulation Engine"

from .network_model import NetworkGraph
from .malware_engine import Malware
from .simulation import Simulator

__all__ = [
    "NetworkGraph",
    "Malware",
    "Simulator",
]

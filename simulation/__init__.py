"""Simulation module for MSpread."""

try:
    from .simulator import Simulator
except ImportError:
    from simulator import Simulator

__all__ = ["Simulator"]

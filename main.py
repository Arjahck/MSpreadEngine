import argparse
import uvicorn
import logging
from typing import Optional
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to allow imports from inside the package
sys.path.insert(0, str(Path(__file__).parent))

from api import create_app
from network_model import NetworkGraph
from malware_engine.malware_base import Worm, Virus, Ransomware, MalwareType
from simulation import Simulator


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main(
    host: str = "127.0.0.1",
    port: int = 8000,
    reload: bool = False,
    mode: str = "api",
    demo: bool = False,
    num_nodes: int = 30000,
    network_type: str = "scale_free",
    malware_type: str = "worm",
    infection_rate: float = 0.35,
    max_steps: int = 50
):
    """
    Entry point for MSpreadEngine application.
    
    Args:
        host: Server IP (default: 127.0.0.1)
        port: Server port (default: 8000)
        reload: Enable auto-reload for development (default: False)
        mode: Execution mode - 'api' or 'demo' (default: 'api')
        demo: Run a demonstration simulation (default: False)
        num_nodes: Number of nodes in demo network (default: 30000)
        network_type: Network topology for demo (default: scale_free)
        malware_type: Malware type for demo (default: worm)
        infection_rate: Infection rate for demo (default: 0.35)
        max_steps: Maximum simulation steps for demo (default: 50)
    """
    logger.info("=" * 60)
    logger.info("MSpreadEngine: Malware Spreading Simulation Engine")
    logger.info("=" * 60)
    
    if demo or mode == "demo":
        logger.info("Running demonstration simulation...")
        run_demo_simulation(
            num_nodes=num_nodes,
            network_type=network_type,
            malware_type=malware_type,
            infection_rate=infection_rate,
            max_steps=max_steps
        )
    else:
        logger.info(f"Starting FastAPI server on {host}:{port}")
        logger.info(f"API Documentation available at http://{host}:{port}/docs")
        logger.info(f"Alternative docs at http://{host}:{port}/redoc")
        
        app = create_app()
        
        try:
            uvicorn.run(
                app,
                host=host,
                port=port,
                reload=reload,
                log_level="info"
            )
        except KeyboardInterrupt:
            logger.info("=" * 60)
            logger.info("Server stopped by user")


def run_demo_simulation(
    num_nodes: int = 30000,
    network_type: str = "scale_free",
    malware_type: str = "worm",
    infection_rate: float = 0.35,
    max_steps: int = 50
):
    """
    Run a demonstration simulation showing malware propagation.
    
    Args:
        num_nodes: Number of nodes in the network
        network_type: Type of network topology (scale_free, small_world, random)
        malware_type: Type of malware (worm, virus, ransomware)
        infection_rate: Infection rate (0-1)
        max_steps: Maximum simulation steps
    """
    logger.info("=" * 60)
    logger.info("DEMONSTRATION SIMULATION")
    logger.info("=" * 60)
    logger.info(f"Parameters: {num_nodes} nodes, {network_type} topology, {malware_type}")
    logger.info(f"Infection rate: {infection_rate}, Max steps: {max_steps}")
    logger.info("-" * 60)
    
    try:
        # Create network
        logger.info(f"[1/5] Creating {network_type} network topology...")
        network = NetworkGraph(network_type=network_type)
        network.generate_topology(num_nodes=num_nodes, use_parallel=True, num_workers=8)
        
        stats = network.get_statistics(skip_expensive=True)
        logger.info(f"    Network created with {stats['num_nodes']} nodes and {stats['num_edges']} edges")
        logger.info(f"    Density: {stats['density']:.4f}")
        
        # Create malware
        logger.info(f"[2/5] Initializing malware ({malware_type.capitalize()})...")
        if malware_type.lower() == "worm":
            malware = Worm("malware_1", infection_rate=infection_rate, latency=1)
        elif malware_type.lower() == "virus":
            malware = Virus("malware_1", infection_rate=infection_rate, latency=2)
        elif malware_type.lower() == "ransomware":
            malware = Ransomware("malware_1", infection_rate=infection_rate, latency=3)
        else:
            raise ValueError(f"Unknown malware type: {malware_type}")
        
        logger.info(f"    Malware type: {malware_type}")
        logger.info(f"    Infection rate: {malware.infection_rate}")
        logger.info(f"    Behavior: {malware.get_behavior()}")
        
        # Initialize simulator
        logger.info("[3/5] Setting up simulator...")
        simulator = Simulator(network, malware)
        initial_infected = ["device_0", "device_1"]
        simulator.initialize(initial_infected)
        logger.info(f"    Initial infection: {initial_infected}")
        
        # Run simulation
        logger.info(f"[4/5] Running simulation (max {max_steps} steps)...")
        simulator.run(max_steps=max_steps)
        
        # Display results
        logger.info("[5/5] Simulation Results")
        logger.info("-" * 60)
        
        stats = simulator.get_statistics()
        logger.info(f"Total Steps:           {stats['total_steps']}")
        logger.info(f"Total Devices:         {stats['total_devices']}")
        logger.info(f"Total Infected:        {stats['total_infected']}")
        logger.info(f"Infection Percentage:  {stats['infection_percentage']:.2f}%")
        logger.info(f"Malware Type:          {stats['malware_type']}")
        
        logger.info("-" * 60)
        logger.info(f"Infection Timeline (first 10 steps):")

        for i, step_data in enumerate(stats['history'][:100]):
            logger.info(
                f"    Step {step_data['step']:3d}: "
                f"Newly Infected: {step_data['newly_infected']:3d}, "
                f"Total Infected: {step_data['total_infected']:3d}"
            )
        
        if len(stats['history']) > 100:
            logger.info(f"... ({len(stats['history']) - 100} more steps)")
        
        logger.info("=" * 60)
        logger.info("Demonstration complete!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error running demonstration: {str(e)}", exc_info=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MSpreadEngine: Malware Spreading Simulation Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py run                                    # Start API server
  python main.py run --host 0.0.0.0                   # Start API on all interfaces
  python main.py run --port 8080                       # Start API on custom port
  python main.py demo                                  # Run demo with defaults (30k nodes, worm, 0.35 rate)
  python main.py demo --nodes 100 --type virus        # Run demo with 100 nodes, virus malware
  python main.py demo --nodes 500 --rate 0.5          # Run demo with higher infection rate
  python main.py demo --topology small_world          # Run demo with small-world topology
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Start the API server")
    run_parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    run_parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    run_parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    run_parser.add_argument("--demo", action="store_true", help="Run demo instead of starting server")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run a demonstration simulation")
    demo_parser.add_argument("--nodes", type=int, default=30000, help="Number of network nodes (default: 30000)")
    demo_parser.add_argument("--topology", default="scale_free", help="Network topology: scale_free, small_world, random (default: scale_free)")
    demo_parser.add_argument("--type", default="worm", help="Malware type: worm, virus, ransomware (default: worm)")
    demo_parser.add_argument("--rate", type=float, default=0.35, help="Infection rate 0-1 (default: 0.35)")
    demo_parser.add_argument("--steps", type=int, default=50, help="Maximum simulation steps (default: 50)")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "run":
        main(
            host=args.host,
            port=args.port,
            reload=args.reload,
            demo=args.demo
        )
    elif args.command == "demo":
        main(
            mode="demo",
            demo=True,
            num_nodes=args.nodes,
            network_type=args.topology,
            malware_type=args.type,
            infection_rate=args.rate,
            max_steps=args.steps
        )
    else:
        parser.print_help()

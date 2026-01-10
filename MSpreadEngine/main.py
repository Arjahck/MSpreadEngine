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
    demo: bool = False
):
    """
    API entry point for MSpread application.
    
    Args:
        host: IP (default: 127.0.0.1)
        port: open port on the ip for the server (default: 8000)
        reload: Enable auto-reload for development (default: False)
        mode: Execution mode - 'api' or 'demo' (default: 'api')
        demo: Run a demonstration simulation (default: False)
    """
    logger.info("=" * 60)
    logger.info("MSpread: Malware Spreading Simulation and Visualization Tool")
    logger.info("=" * 60)
    
    if demo or mode == "demo":
        logger.info("Running demonstration simulation...")
        run_demo_simulation()
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


def run_demo_simulation():
    """
    Run a demonstration simulation showing malware propagation.
    
    This function creates a sample network, initializes malware,
    and runs a simulation to show the spreading behavior.
    """
    logger.info("=" * 60)
    logger.info("DEMONSTRATION SIMULATION")
    logger.info("=" * 60)
    
    try:
        # Create a scale-free network
        logger.info("[1/5] Creating network topology...")
        network = NetworkGraph(network_type="scale_free")
        network.generate_topology(num_nodes=30000, use_parallel=True, num_workers=8)
        
        stats = network.get_statistics(skip_expensive=True)  # Skip expensive calculations for large networks
        logger.info(f"    Network created with {stats['num_nodes']} nodes and {stats['num_edges']} edges")
        logger.info(f"    Density: {stats['density']:.4f}")
        
        # Create worm malware
        logger.info("[2/5] Initializing malware (Worm)...")
        malware = Worm("worm_1", infection_rate=0.35, latency=1)
        logger.info(f"    Malware created with infection rate: {malware.infection_rate}")
        logger.info(f"    Behavior: {malware.get_behavior()}")
        
        # Initialize simulator
        logger.info("[3/5] Setting up simulator...")
        simulator = Simulator(network, malware)
        initial_infected = ["device_0", "device_1"]
        simulator.initialize(initial_infected)
        logger.info(f"    Initial infection: {initial_infected}")
        
        # Run simulation
        logger.info("[4/5] Running simulation...")
        simulator.run(max_steps=50)
        
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
        description="MSpread: Malware Spreading Simulation and Visualization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py run                       # Start API server
  python main.py run --host 0.0.0.0       # Start API on all interfaces
  python main.py run --port 8080           # Start API on custom port
  python main.py demo                      # Run demonstration simulation
  python main.py run --demo                # Alternative demo command
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Start the API server")
    run_parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    run_parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    run_parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    run_parser.add_argument("--demo", action="store_true", help="Run demonstration simulation")
    
    # Demo command
    subparsers.add_parser("demo", help="Run a demonstration simulation")
    
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
        main(mode="demo", demo=True)
    else:
        parser.print_help()

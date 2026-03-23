import os
import sys
import time
import logging
import asyncio
from swarmledger.consensus import ConsensusEngine
from swarmledger.swarm_coordinator import SwarmCoordinator
from swarmledger.policy_engine import PolicyEngine

logging.basicConfig(level=logging.INFO)

async def main():
    """Main entry point for the SwarmLedger platform."""
    consensus_engine = ConsensusEngine()
    policy_engine = PolicyEngine()
    swarm_coordinator = SwarmCoordinator(consensus_engine, policy_engine)

    await swarm_coordinator.start()

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
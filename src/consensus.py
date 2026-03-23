# Byzantine Fault Tolerant Consensus for Swarm Decision Making
import hashlib
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from time import time

@dataclass
class ConsensusProposal:
    proposal_id: str
    proposer: str
    timestamp: float
    value: dict
    signatures: Dict[str, str] = None

class SwarmConsensus:
    def __init__(self, node_id: str, min_quorum: float = 0.67):
        self.node_id = node_id
        self.min_quorum = min_quorum
        self.proposals: Dict[str, ConsensusProposal] = {}
        self.votes: Dict[str, Set[str]] = {}
        self.finalized: Dict[str, ConsensusProposal] = {}
    
    def propose(self, value: dict) -> ConsensusProposal:
        """Create a new consensus proposal"""
        proposal_id = hashlib.sha256(
            f"{self.node_id}:{time()}:{str(value)}".encode()
        ).hexdigest()
        
        proposal = ConsensusProposal(
            proposal_id=proposal_id,
            proposer=self.node_id,
            timestamp=time(),
            value=value,
            signatures={}
        )
        
        self.proposals[proposal_id] = proposal
        self.votes[proposal_id] = set([self.node_id])
        return proposal

    def vote(self, proposal_id: str, voter_id: str, signature: str) -> bool:
        """Register a vote for a proposal"""
        if proposal_id not in self.proposals:
            return False
            
        if voter_id in self.votes[proposal_id]:
            return False
            
        self.votes[proposal_id].add(voter_id)
        self.proposals[proposal_id].signatures[voter_id] = signature
        
        return True

    def is_finalized(self, proposal_id: str, total_nodes: int) -> bool:
        """Check if proposal has reached consensus"""
        if proposal_id not in self.proposals:
            return False
            
        votes = len(self.votes[proposal_id])
        required_votes = int(total_nodes * self.min_quorum)
        
        if votes >= required_votes:
            self.finalized[proposal_id] = self.proposals[proposal_id]
            return True
            
        return False

    def get_proposal(self, proposal_id: str) -> ConsensusProposal:
        """Retrieve a proposal by ID"""
        return self.proposals.get(proposal_id)

    def get_finalized(self) -> Dict[str, ConsensusProposal]:
        """Get all finalized proposals"""
        return self.finalized.copy()

    def cleanup_old_proposals(self, max_age: float = 3600):
        """Remove proposals older than max_age seconds"""
        current_time = time()
        expired = [
            pid for pid, p in self.proposals.items()
            if current_time - p.timestamp > max_age
        ]
        
        for pid in expired:
            if pid not in self.finalized:
                del self.proposals[pid]
                del self.votes[pid]
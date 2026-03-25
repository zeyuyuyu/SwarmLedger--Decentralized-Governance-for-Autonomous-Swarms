# Byzantine Fault Tolerant Consensus Implementation for SwarmLedger
import time
from typing import Dict, List, Set
import hashlib
from dataclasses import dataclass
from enum import Enum

class VoteType(Enum):
    PREPARE = 1
    COMMIT = 2
    
@dataclass
class Vote:
    node_id: str
    proposal_hash: str
    timestamp: float
    vote_type: VoteType
    signature: str
    weight: float

class BFTConsensus:
    def __init__(self, node_id: str, total_nodes: int, required_quorum: float = 0.67):
        self.node_id = node_id
        self.total_nodes = total_nodes
        self.required_quorum = required_quorum
        self.proposals: Dict[str, any] = {}
        self.prepare_votes: Dict[str, Set[Vote]] = {}
        self.commit_votes: Dict[str, Set[Vote]] = {}
        self.finalized_proposals: Set[str] = set()
        self.node_weights: Dict[str, float] = {}
    
    def set_node_weights(self, weights: Dict[str, float]) -> None:
        """Set voting weights for nodes based on reputation/stake"""
        self.node_weights = weights
        
    def propose(self, proposal: any) -> str:
        """Create a new proposal for consensus"""
        proposal_hash = hashlib.sha256(str(proposal).encode()).hexdigest()
        self.proposals[proposal_hash] = proposal
        self.prepare_votes[proposal_hash] = set()
        self.commit_votes[proposal_hash] = set()
        return proposal_hash

    def vote(self, proposal_hash: str, vote_type: VoteType) -> Vote:
        """Cast a vote for a proposal"""
        if proposal_hash not in self.proposals:
            raise ValueError('Unknown proposal')
            
        vote = Vote(
            node_id=self.node_id,
            proposal_hash=proposal_hash,
            timestamp=time.time(),
            vote_type=vote_type,
            signature=self._sign_vote(proposal_hash, vote_type),
            weight=self.node_weights.get(self.node_id, 1.0)
        )
        
        if vote_type == VoteType.PREPARE:
            self.prepare_votes[proposal_hash].add(vote)
        else:
            self.commit_votes[proposal_hash].add(vote)
            
        return vote

    def receive_vote(self, vote: Vote) -> None:
        """Process received vote from another node"""
        if not self._verify_vote(vote):
            raise ValueError('Invalid vote signature')
            
        if vote.vote_type == VoteType.PREPARE:
            self.prepare_votes[vote.proposal_hash].add(vote)
        else:
            self.commit_votes[vote.proposal_hash].add(vote)

    def check_consensus(self, proposal_hash: str) -> bool:
        """Check if consensus has been reached for a proposal"""
        if proposal_hash in self.finalized_proposals:
            return True
            
        prepare_weight = sum(v.weight for v in self.prepare_votes[proposal_hash])
        commit_weight = sum(v.weight for v in self.commit_votes[proposal_hash])
        
        total_weight = sum(self.node_weights.values())
        quorum_weight = total_weight * self.required_quorum
        
        if prepare_weight >= quorum_weight and commit_weight >= quorum_weight:
            self.finalized_proposals.add(proposal_hash)
            return True
            
        return False

    def get_proposal(self, proposal_hash: str) -> any:
        """Retrieve a proposal by its hash"""
        return self.proposals.get(proposal_hash)

    def _sign_vote(self, proposal_hash: str, vote_type: VoteType) -> str:
        """Sign a vote with the node's private key"""
        # TODO: Implement actual cryptographic signing
        return f'{self.node_id}:{proposal_hash}:{vote_type.value}'

    def _verify_vote(self, vote: Vote) -> bool:
        """Verify a vote's signature"""
        # TODO: Implement actual signature verification
        expected = f'{vote.node_id}:{vote.proposal_hash}:{vote.vote_type.value}'
        return vote.signature == expected
import hashlib
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from time import time

@dataclass
class Vote:
    proposal_id: str
    voter_id: str
    weight: float
    timestamp: float
    signature: str

@dataclass 
class Proposal:
    id: str
    content: dict
    timestamp: float
    proposer: str

class ByzantineConsensus:
    def __init__(self, node_id: str, voting_weights: Dict[str, float]):
        self.node_id = node_id
        self.voting_weights = voting_weights
        self.proposals: Dict[str, Proposal] = {}
        self.votes: Dict[str, Set[Vote]] = {}
        self.decided_proposals: Set[str] = set()
        self.quorum_threshold = 0.67

    def create_proposal(self, content: dict) -> Proposal:
        """Create a new proposal to be voted on"""
        proposal_id = hashlib.sha256(
            f"{content}{time()}{self.node_id}".encode()
        ).hexdigest()
        
        proposal = Proposal(
            id=proposal_id,
            content=content,
            timestamp=time(),
            proposer=self.node_id
        )
        
        self.proposals[proposal_id] = proposal
        self.votes[proposal_id] = set()
        return proposal

    def vote(self, proposal_id: str) -> Vote:
        """Cast a vote for a proposal"""
        if proposal_id not in self.proposals:
            raise ValueError(f"Unknown proposal {proposal_id}")
            
        vote = Vote(
            proposal_id=proposal_id,
            voter_id=self.node_id,
            weight=self.voting_weights.get(self.node_id, 0),
            timestamp=time(),
            signature=self._sign_vote(proposal_id)
        )
        
        self.votes[proposal_id].add(vote)
        return vote

    def receive_vote(self, vote: Vote) -> bool:
        """Process a vote received from another node"""
        if not self._verify_vote(vote):
            return False
            
        if vote.proposal_id not in self.votes:
            self.votes[vote.proposal_id] = set()
            
        self.votes[vote.proposal_id].add(vote)
        return True

    def is_decided(self, proposal_id: str) -> Tuple[bool, bool]:
        """Check if a proposal has reached consensus
        Returns: (is_decided, accepted)"""
        if proposal_id not in self.proposals:
            return False, False
            
        if proposal_id in self.decided_proposals:
            return True, True

        total_weight = 0
        for vote in self.votes[proposal_id]:
            total_weight += vote.weight

        if total_weight >= sum(self.voting_weights.values()) * self.quorum_threshold:
            self.decided_proposals.add(proposal_id)
            return True, True

        return False, False

    def _sign_vote(self, proposal_id: str) -> str:
        """Create signature for a vote"""
        return hashlib.sha256(
            f"{proposal_id}{self.node_id}{time()}".encode()
        ).hexdigest()

    def _verify_vote(self, vote: Vote) -> bool:
        """Verify vote signature and weight"""
        if vote.voter_id not in self.voting_weights:
            return False
            
        if vote.weight != self.voting_weights[vote.voter_id]:
            return False
            
        # In production, verify cryptographic signature here
        return True

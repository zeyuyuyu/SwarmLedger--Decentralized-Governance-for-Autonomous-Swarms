import time
import hashlib
import random

class Validator:
    def __init__(self, address, stake):
        self.address = address
        self.stake = stake
        self.last_block_time = 0

    def validate_block(self, block):
        # Validate block timestamp and previous hash
        if block['timestamp'] <= self.last_block_time:
            return False
        if block['prev_hash'] != self.compute_hash(self.last_block):
            return False

        # Validate block proposer
        if block['proposer'] != self.address:
            return False

        # Update validator state
        self.last_block_time = block['timestamp']
        self.last_block = block
        return True

    def compute_hash(self, block):
        block_string = str(block)
        return hashlib.sha256(block_string.encode()).hexdigest()

class ConsensusManager:
    def __init__(self):
        self.validators = []
        self.chain = []

    def add_validator(self, validator):
        self.validators.append(validator)

    def propose_block(self):
        # Select a validator to propose the next block
        validator = random.choice(self.validators)

        # Create the new block
        block = {
            'timestamp': time.time(),
            'proposer': validator.address,
            'transactions': [],
            'prev_hash': self.compute_hash(self.chain[-1])
        }

        # Validate the block
        if validator.validate_block(block):
            self.chain.append(block)
            return block
        else:
            return None

    def compute_hash(self, block):
        block_string = str(block)
        return hashlib.sha256(block_string.encode()).hexdigest()

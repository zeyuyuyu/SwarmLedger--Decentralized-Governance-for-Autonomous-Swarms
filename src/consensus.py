import random
import time

class SwarmConsensus:
    def __init__(self, swarm_size, decision_threshold):
        self.swarm_size = swarm_size
        self.decision_threshold = decision_threshold
        self.swarm_state = [0] * swarm_size
        self.last_update_time = time.time()

    def update_swarm_state(self, agent_index, new_state):
        self.swarm_state[agent_index] = new_state
        self.last_update_time = time.time()

    def get_swarm_decision(self):
        if time.time() - self.last_update_time > 60:
            return None

        positive_votes = sum(1 for state in self.swarm_state if state == 1)
        negative_votes = sum(1 for state in self.swarm_state if state == 0)

        if positive_votes >= self.decision_threshold:
            return 1
        elif negative_votes >= self.decision_threshold:
            return 0
        else:
            return None

    def simulate_swarm_behavior(self):
        while True:
            agent_index = random.randint(0, self.swarm_size - 1)
            new_state = random.randint(0, 1)
            self.update_swarm_state(agent_index, new_state)
            swarm_decision = self.get_swarm_decision()
            if swarm_decision is not None:
                print(f'Swarm decision: {swarm_decision}')
                break
            time.sleep(1)

class MinimizedDFA:
    def __init__(self, states, transitions, accepting_states):
        self.states = states
        self.transitions = transitions
        self.accepting_states = accepting_states
        self.initial_state = 1  # Assuming 1 is the initial state

    def is_match(self, word):
        current_state = self.initial_state
        for char in word:
            if current_state not in self.transitions or char not in self.transitions[current_state]:
                return False
            current_state = self.transitions[current_state][char]
        return current_state in self.accepting_states
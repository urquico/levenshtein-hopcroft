from collections import deque, defaultdict

def hopcroft(dfa):
    # Step 1: Initialize variables and data structures
    states, transitions = set(), defaultdict(dict)
    matching_states = set()

    # Step 2: Create a queue and enqueue the start state
    queue = deque([dfa.start()])

    # Step 3: Perform the BFS-based Hopcroft's algorithm
    while queue:
        current_state = queue.popleft()

        if current_state in states:
            continue

        states.add(current_state)

        if dfa.is_match(current_state):
            matching_states.add(current_state)

        for transition in dfa.transitions(current_state):
            next_state = dfa.step(current_state, transition)

            if next_state not in states:
                queue.append(next_state)

            transitions[current_state][transition] = next_state

    # Step 4: Return the states, transitions, and matching states
    return states, transitions, matching_states
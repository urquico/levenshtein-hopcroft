import csv
from DFA import DFA
from hopcroft import hopcroft

tagalogWords = []
maxEdit = 1
uniqueCharacters = {}
totalReductionRate_states = 0
totalReductionRate_transitions = 0

# source: https://github.com/raymelon/tagalog-dictionary-scraper
with open('./tagalog_dict.csv', 'r') as file:
    csvReader = csv.reader(file)
    for row in csvReader:
        tagalogWords.append(row[0].lower())  # appending the rows of the csv file into tagalogWords variable

uniqueCharacters = set(''.join(tagalogWords))

for word in tagalogWords:

    counter = [0]
    states = {}
    transitions = []
    matching = []
    lev = DFA(word, maxEdit)
    # Generate the initial state
    levState = lev.start()

    # minimized DFA using Hopcroft's Algorithm
    minimized_states, minimized_transitions, minimized_matching = hopcroft(lev)


    def explore(state):
        key = (tuple(state[0]),
               tuple(state[1]))  # lists can't be hashed in Python because they are mutable, so convert to a tuple
        if key in states:
            return states[key]
        i = counter[0]
        counter[0] += 1
        states[key] = i
        if lev.is_match(state):
            matching.append(i)
        for c in lev.transitions(state) | {'*'}:
            newstate = lev.step(state, c)
            j = explore(newstate)
            transitions.append((i, j, c))
        return i


    explore(levState)
    # ReductionRateStates = (Initial Number of States - Final Number of States) / InitialNumberofStates * 100
    # ReductionRateTransitions = (Initial Number of Transitions - Final Number of Transitions) / InitialNumberofTransitions * 100

    reductionRateStates = (len(states) - len(minimized_states)) / len(states) * 100
    reductionRateTransitions = (len(transitions) - len(minimized_transitions)) / len(transitions) * 100
    totalReductionRate_states += reductionRateStates
    totalReductionRate_transitions += reductionRateTransitions

print("n = ", len(tagalogWords))
print("k = ", maxEdit)
print("|Σ| = ", len(uniqueCharacters))
print(sorted(uniqueCharacters))
print("Reduction Rate (States) = ", totalReductionRate_states / len(tagalogWords))
print("Reduction Rate (Transitions) = ", totalReductionRate_transitions / len(tagalogWords))

import csv
import shutil
from helper import removePunctuation, removeAdjacentLetters, writeGraphs, count_transitions, writeMinimizedGraphs
from DFA import DFA
from hopcroft import hopcroft

suggestedWords = []
tagalogWords = []
statement = "An darting ang mga salta"
statement = removePunctuation(statement).lower()

maxEdit = 1
directory = "./DFA_Graph"
minimizedDirectory = "./MIN_DFA_Graph"

# remove the DFA_Graph Folder
shutil.rmtree(directory, ignore_errors=True)
shutil.rmtree(minimizedDirectory, ignore_errors=True)

# source: https://github.com/raymelon/tagalog-dictionary-scraper
with open('./tagalog_dict.csv', 'r') as file:
    csvReader = csv.reader(file)
    for row in csvReader:
        tagalogWords.append(row[0].lower())  # appending the rows of the csv file into tagalogWords variable

for word in statement.split():

    counter = [0]
    states = {}
    transitions = []
    matching = []
    lev = DFA(removeAdjacentLetters(word), maxEdit)
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
    suggestedWords = []

    for tagalogWord in tagalogWords:
        levState = lev.start()
        for letter in tagalogWord:
            levState = lev.step(levState, letter)

        # Check if the input word can potentially match the desired Levenshtein distance
        if lev.can_match(levState):
            if word != tagalogWord and len(tagalogWord) >= len(word):
                suggestedWords.append(tagalogWord)

    print("--RESULTS-------------------------------------")
    transitions.sort(key=lambda x: x[0])

    # graphviz utilization
    writeGraphs(word, transitions, matching, directory, maxEdit)
    writeMinimizedGraphs(word, minimized_transitions, minimized_matching, minimizedDirectory, maxEdit)

    if len(suggestedWords) != 0:
        # print(f"Suggested Words for '{word}': ", suggestedWords)
        print(f"'{len(suggestedWords)}' Suggested Words for '{word}': ")
    else:
        print(f"No Suggested Words for '{word}'")
    print("Number of States: from ", counter, "to", len(minimized_states))
    print("Number of Transitions: from ", len(transitions), "to", count_transitions(minimized_transitions))
    print("Number of Accepting States: from ", len(matching), "to", len(minimized_matching))
    print("--------------- Suggested Words --------------")
    max_width = 45
    current_width = 0

    for word in suggestedWords:
        if current_width + len(word) + 1 <= max_width:
            print(word, end=", ")
            current_width += len(word) + 2  # Adding 2 for the word and comma
        else:
            print()
            print(word, end=", ")
            current_width = len(word) + 2  # Adding 2 for the word and comma

    print()
    print("-------------------- END ---------------------")








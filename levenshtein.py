import csv
import os
import shutil
from helper import removePunctuation, removeAdjacentLetters
from DFA import DFA

suggestedWords = []
tagalogWords = []
statement = "an darting ang mga salta"
statement = removePunctuation(statement).lower()

maxEdit = 1
directory = "./DFA_Graph"

# remove the DFA_Graph Folder
shutil.rmtree(directory, ignore_errors=True)

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
    lev = DFA(removeAdjacentLetters(word), 1)
    # Generate the initial state
    levState = lev.start()


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

    print("----------------------------------------------")
    transitions.sort(key=lambda x: x[0])

    # output to graphviz
    filename = removeAdjacentLetters(word) + ".dot"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)

    f = open(file_path, "w")
    f.write("digraph G {")
    for t in transitions:
        f.write('\n\t%s -> %s [label=" %s "]' % t)
    for i in matching:
        f.write('\n\t%s [style=filled]' % i)
    f.write("\n}")

    if len(suggestedWords) != 0:
        print(f"Suggested Words for '{word}': ", suggestedWords)
    else:
        print(f"No Suggested Words for '{word}'")
    print("Number of States: ", counter)
    print("Number of Transitions", len(transitions))
    print("Number of Accepting States", len(matching))
    print("----------------------------------------------")

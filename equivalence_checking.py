import csv
from helper import removePunctuation, removeAdjacentLetters, get_unique_states, convert_transitions, \
    convert_matching_states
from MinimizedDFA import MinimizedDFA
from DFA import DFA
from hopcroft import hopcroft

suggestedWords = []
min_suggestedWords = []
tagalogWords = []
statement = "an darting ang mga salta"
statement = removePunctuation(statement).lower()

maxEdit = 1

# source: https://github.com/raymelon/tagalog-dictionary-scraper
with open('./tagalog_dict.csv', 'r') as file:
    csvReader = csv.reader(file)
    for row in csvReader:
        tagalogWords.append(row[0].lower())  # appending the rows of the csv file into tagalogWords variable

for word in statement.split():
    lev = DFA(removeAdjacentLetters(word), maxEdit)
    # Generate the initial state
    levState = lev.start()

    # minimized DFA using Hopcroft's Algorithm
    minimized_states, minimized_transitions, minimized_matching = hopcroft(lev)
    # initial_state = 0
    converted_transitions = convert_transitions(minimized_transitions)
    converted_states = get_unique_states(minimized_states)
    converted_matching = convert_matching_states(minimized_matching)
    # print(len(minimized_transitions), convert_transitions(minimized_transitions))
    # print(len(minimized_states), get_unique_states(minimized_states))
    # print(len(minimized_matching), convert_matching_states(minimized_matching))
    minimized_dfa = MinimizedDFA(converted_states, converted_transitions, converted_matching)
    # print(converted_states)
    # print(converted_transitions)
    # print(converted_matching)
    # print(initial_state)

    suggestedWords = []

    for tagalogWord in tagalogWords:
        levState = lev.start()

        for letter in tagalogWord:
            levState = lev.step(levState, letter)

        # Check if the input word can potentially match the desired Levenshtein distance
        if lev.can_match(levState):
            if word != tagalogWord and len(tagalogWord) >= len(word):
                suggestedWords.append(tagalogWord)

        is_match = minimized_dfa.is_match(tagalogWord)  # minimized dfa equivalence checking
        if is_match and word != tagalogWord:
            min_suggestedWords.append(tagalogWord)

    print("--------------- Suggested Words --------------")
    max_width = 45
    current_width = 0
    print(len(suggestedWords))
    for word in suggestedWords:
        if current_width + len(word) + 1 <= max_width:
            print(word, end=", ")
            current_width += len(word) + 2  # Adding 2 for the word and comma
        else:
            print()
            print(word, end=", ")
            current_width = len(word) + 2  # Adding 2 for the word and comma

    print()
    print("----------------------------------------------")

    current_width = 0
    print(len(suggestedWords))
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

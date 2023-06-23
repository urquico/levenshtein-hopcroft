import string
import re
import os


def removePunctuation(text):
    # Create a translation table mapping punctuation marks to None
    translator = str.maketrans("", "", string.punctuation)

    # Remove punctuation using the translation table
    noPunct = text.translate(translator)

    return noPunct


def removeAdjacentLetters(text):
    pattern = r'(\w)\1+'  # Pattern to match adjacent repeated letters

    # Use the sub() function to replace the matched pattern with a single occurrence
    cleanedString = re.sub(pattern, r'\1', text)

    return cleanedString


def count_transitions(transitions):
    num_transitions = 0

    for source_state, next_states in transitions.items():
        for input_symbol, next_state in next_states.items():
            num_transitions += 1

    return num_transitions


def writeGraphs(word, transitions, matching, directory, k):
    # output to graphviz
    filename = removeAdjacentLetters(word) + "_kEdit-" + str(k) + ".dot"
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


def writeMinimizedGraphs(word, transitions, matching, directory, k):
    dot_script = "digraph G {\n"
    state_mapping = {}  # Mapping for original states to single digits/characters
    counter = 0

    for source_state, actions in transitions.items():
        source_state_str = state_mapping.setdefault(source_state, str(counter))
        counter += 1
        for action, next_state in actions.items():
            next_state_str = state_mapping.setdefault(next_state, str(counter))
            counter += 1
            dot_script += f"\ts{source_state_str} -> s{next_state_str} [label=\" {action} \"]\n"

    for matching_state in matching:
        matching_state_str = state_mapping.setdefault(matching_state, str(counter))
        counter += 1
        dot_script += f"\ts{matching_state_str} [style=filled]\n"

    dot_script += "}"

    # output to graphviz
    filename = removeAdjacentLetters(word) + "_minimized" + "_kEdit-" + str(k) + ".dot"
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, filename)
    f = open(file_path, "w")
    f.write(dot_script)

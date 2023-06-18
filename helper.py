import string
import re

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
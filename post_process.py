#Text preprocessing
#spell-checking, grammar correction, removing non-textual elements
import re
def text_process(text):
    stripped_text = re.sub(r'([^\s\w]|_)+', '', text)
    return stripped_text
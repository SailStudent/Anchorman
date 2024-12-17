import textwrap

def wrap_text(text, width):
    return '\n'.join(textwrap.wrap(text, width))
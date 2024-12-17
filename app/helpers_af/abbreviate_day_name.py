from static._DAY_ABBREVIATIONS import _DAY_ABBREVIATIONS

def abbreviate_day_name(text):
    for full_day, abbr_day in _DAY_ABBREVIATIONS.items():
        text = text.replace(full_day, abbr_day)
    return text
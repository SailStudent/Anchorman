from static._DAY_ABBREVIATIONS import _DAY_ABBREVIATIONS

def extract_day_name(period_name):
    for full_day in _DAY_ABBREVIATIONS.keys():
        if (full_day.lower() in period_name.lower()) or (_DAY_ABBREVIATIONS[full_day].lower() in period_name.lower()):
            return full_day
    return None
def format_time_to_zulu(dt):
    if dt is None:
        return None
    return dt.strftime("%H:%M Z")
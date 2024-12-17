from bs4 import BeautifulSoup

# Weather abbreviations mapping
WEATHER_FX = {
    'RA': 'Rain',
    'SN': 'Snow',
    'FZRA': 'Freezing Rain',
    'TSTMS': 'Thunderstorms',
    'VCNTY': 'Vicinity'
}

def get_af_precipitation(html_file, start_day, num_days):
    soup = BeautifulSoup(html_file, 'html.parser')
    
    # Collecting the precipitation data
    forecast_div = soup.find('div', id='forecast_div')
    percip_table = forecast_div.find_all('td', class_='test2 forecast')[34:51]
    percip_section = [percip.get_text(strip=True) for percip in percip_table]

    # Handle cases where abbreviations like 'TSTMSVCNTY' are present
    def parse_precipitation(precip_str):
        # Check if it's a valid percentage, otherwise return None
        try:
            return int(precip_str.strip('%')) if precip_str.isdigit() else None
        except ValueError:
            return None

    percip_values = [parse_precipitation(perc) for perc in percip_section]

    # Group data by time (AM/PM) and store in a dictionary by forecast hour
    forecast_table = forecast_div.find_all('td', class_='test2 time')
    forecast_times = [int(forecast.get_text(strip=True)[:2]) for forecast in forecast_table]

    percip_dict = {}
    for i, time in enumerate(forecast_times):
        if time not in percip_dict:
            percip_dict[time] = [percip_values[i]]
        else:
            percip_dict[time].append(percip_values[i])

    # Replace any empty precipitation values with None
    for key, values in percip_dict.items():
        percip_dict[key] = [None if val == '' else val for val in values]

    # Calculate the ratio of non-None precipitation values for each time
    new_dict = {}
    for key, values in percip_dict.items():
        count_none = values.count(None)
        if count_none < len(values):
            ratio = 1 - (count_none / len(values))
            new_dict[key] = ratio
        else:
            new_dict[key] = 0  # If all are None, precipitation is 0%

    percip_list = [value for key, value in new_dict.items()]

    # Calculate the precipitation average based on the selected days
    start_index = (start_day - 1) * 2  # Adjust for AM/PM indexing
    end_index = start_index + num_days * 2

    selected_precip_values = percip_list[start_index:end_index]
    
    if selected_precip_values:
        average_precipitation = sum(selected_precip_values) / len(selected_precip_values)
    else:
        average_precipitation = 0  # No precipitation data available
    
    # Return the precipitation in a user-friendly format
    if num_days == 1:
        return f'{int(average_precipitation * 100)}% precip probability'
    else:
        min_precip = int(min(selected_precip_values) * 100)
        max_precip = int(max(selected_precip_values) * 100)
        if min_precip == max_precip:
            return f'{min_precip}% precip probability'
        else:
            return f'{min_precip}-{max_precip}% precip probability'


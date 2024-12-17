import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from math import ceil

import pandas as pd


from helpers_af.create_af_forecast_df import create_af_forecast_df

def df_for_slide(forecast_data):

    # Parse and structure the forecast data into a DataFrame
    forecast_dict = {
        "Day": [],
        "Time": [],
        "Graphic": [],
        "Temp": [],
        "Wind": [],
        "Gusts": []
    }

    for i in range(len(forecast_data['Day'])):
        forecast_dict["Day"].append(forecast_data['Day'][i])
        forecast_dict["Time"].append(forecast_data['Time'][i])
        forecast_dict["Temp"].append(forecast_data['Temps'][i])
        forecast_dict["Wind"].append(forecast_data['Winds'][i])
        forecast_dict["Gusts"].append(forecast_data['Gusts'][i])
    
    
    
    
    

    forecast_dict['Wind'] = [wind.replace('at', '@') for wind in forecast_dict['Wind']]
    forecast_dict['Day'] = [day[:4] for day in forecast_dict['Day']]
  
    forecast_comb = {"Full Forecast": [(row["Forecast"] + " - " + row["Details"]).lower() for _, row in forecast_data.iterrows()]}
    for i in range(len(forecast_comb["Full Forecast"])):       
        if "cloudy" in forecast_comb["Full Forecast"][i] and "thunderstorms" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("⛈")
        elif "cloudy" in forecast_comb["Full Forecast"][i] and "showers" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("🌧")
        elif "cloudy" in forecast_comb["Full Forecast"][i] and "partly" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("⛅")
        elif "cloudy" in forecast_comb["Full Forecast"][i] or "haze" in forecast_comb["Full Forecast"][i] or "fog" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("☁")
        elif "chance" in forecast_comb["Full Forecast"][i] and "showers" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("🌦")
        elif "shower" in forecast_comb["Full Forecast"][i] and "thunderstorms" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("⛈")
        elif "sunny" in forecast_comb["Full Forecast"][i] and "showers" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("🌦")
        elif "showers" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("🌧")
        elif "partly sunny" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("⛅")
        elif "mostly sunny" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("⛅")
        elif "sunny" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("😎")
        elif "clear" in forecast_comb["Full Forecast"][i]:
            forecast_dict["Graphic"].append("😎")
        else:
            forecast_dict["Graphic"].append("❓")
    

    if len(forecast_dict['Day']) == 10:
        forecast_dict['Day'] = forecast_dict['Day'][1:]
        forecast_dict['Time'] = forecast_dict['Time'][1:]
        
        forecast_dict['Temp'] = forecast_dict['Temp'][1:]
        forecast_dict['Wind'] = forecast_dict['Wind'][1:]
        forecast_dict['Gusts'] = forecast_dict['Gusts'][1:]
        forecast_dict['Graphic'] = forecast_dict['Graphic'][1:]
    else:
        forecast_dict['Day'] = forecast_dict['Day']
        forecast_dict['Time'] = forecast_dict['Time']
        
        forecast_dict['Temp'] = forecast_dict['Temp']
        forecast_dict['Wind'] = forecast_dict['Wind']
        forecast_dict['Gusts'] = forecast_dict['Gusts']
        forecast_dict['Graphic'] = forecast_dict['Graphic']


    forecast_dict['Day'][0] = 'Today'
    forecast_df = pd.DataFrame(forecast_dict).T
    return forecast_df


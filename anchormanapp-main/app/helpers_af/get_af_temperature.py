import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers_af.create_af_forecast_df import create_af_forecast_df
from services.get_af_weather_html import get_af_weather_html

def get_af_temperature(forecast_df, num_days):
    temperatures = forecast_df['Temps'].tolist()
    temperatures = [int("".join(filter(str.isdigit, temp))) for temp in temperatures]
    
    avg_temp = []
    if len(temperatures) ==10:
        start_iter = 0
    else:
        avg_temp.append(temperatures[0])
        start_iter = 1
    for i in range(start_iter, len(temperatures), 2):
        temp1 = temperatures[i]
        temp2 = temperatures[i+1]
        average = (temp1 + temp2) / 2
        avg_temp.append(int(average))

    a_temps=0
    for i in range(num_days):
        a_temps+=avg_temp[i]
    a_temps = a_temps/num_days

    return f'Average {a_temps:.1f}F'
  

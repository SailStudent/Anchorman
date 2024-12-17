import pandas as pd
import re
from bs4 import BeautifulSoup

def create_af_forecast_df(html_content):
    
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    forecast_5_day = soup.find('div', id='five_day')

    if forecast_5_day.find('td', class_='table_subheader_sm', colspan='1'):        
        header_info = forecast_5_day.find_all('td', class_='table_subheader_sm', colspan='2')
        header_info.insert(0, forecast_5_day.find('td', class_='table_subheader_sm', colspan='1'))
        header_info = [header.get_text(strip=True) for header in header_info]
        
        headers = [header for header in header_info for _ in range(2)]
        headers.pop(0)
       

        header_dict = {"Day": headers}
        time_of_day = {"Time": ["AM", "PM"] * 4}
        time_of_day["Time"].insert(0, "PM")

        # Getting the temperatures, Wind, and Gusts for each day    
        temps_list = forecast_5_day.find_all('td', class_='test2')
        items = [temp.get_text(strip=True) for temp in temps_list]
        temps = {"Temps": items[:9]}
        wind = {"Winds":items[9:18]}
        gusts = {"Gusts": items[18:27]}
    else:
        header_info = forecast_5_day.find_all('td', class_='table_subheader_sm', colspan='2')
        header_info = [header.get_text(strip=True) for header in header_info]

        headers = [header for header in header_info for _ in range(2)]
        header_dict = {"Day": headers}
        time_of_day = {"Time": ["AM", "PM"] * 5}

        # Getting the temperatures, Wind, and Gusts for each day  
        temps_list = forecast_5_day.find_all('td', class_='test2')
        items = [temp.get_text(strip=True) for temp in temps_list]
        temps = {"Temps": items[:10]}
        wind = {"Winds":items[10:20]}
        gusts = {"Gusts": items[20:31]}



    # Find the forecast data (Verbal)
    forecast_data = forecast_5_day.find_all('td', class_='test bold')
    forecast_values = [data.get_text(strip=True) for data in forecast_data]
    daily_forecast = {"Forecast": forecast_values}

    # Find the forecast details
    forecast_details_section = forecast_5_day.find('tr', class_='bottomborder')
    forecast_details = forecast_details_section.find_all('td', class_='test')
    forecast_details = [detail.get_text(strip=True) for detail in forecast_details]
    forecast_details = {"Details": forecast_details}

    
    overall_forecast = {**header_dict, **time_of_day, **daily_forecast, **forecast_details, **temps, **wind, **gusts}


    
   
    # Create a DF
    df = pd.DataFrame.from_dict(overall_forecast)

    forecast_data = pd.DataFrame({
        "Full Forecast": [row["Forecast"] + " - " + row["Details"] for _, row in df.iterrows()]
    })
    
    return df


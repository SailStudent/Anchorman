from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helpers_af.abbreviate_day_name import abbreviate_day_name


def create_af_illum_dataframe(html_content):    
    
    today = datetime.utcnow().date()
    date_range = [today + timedelta(days=i) for i in range(3)]
    
    header_data = {}

    # Parse the HTML content
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find and pull the div class="solar"
    suntable = soup.find('table', class_='suntable')
    if suntable is None:
        raise ValueError("The specified element with class='suntable' was not found in the HTML.")

    # Access the content of the div
    solar_content = suntable.text.strip()

    # Find and pull the th class="span_subheader_sm"
    span_subheader_sm = soup.find_all('th', class_='span_subheader_sm')
    if span_subheader_sm is None:
        raise ValueError("The specified element with class='span_subheader_sm' was not found in the HTML.")

    illum_info = suntable.find_all('td', class_='test2')
    if illum_info is None:
        raise ValueError("The specified element with class='test2' was not found in the HTML.")
    
    for k in range(0,3):
        illum_list = []
        illum_info = suntable.find_all('td', class_='test2')
        if k==0:
            range_start =0
            range_end = 10
        elif k==1:
            range_start =10
            range_end = 20
        elif k==2:
            range_start =20
            range_end = 30
        for data in illum_info[range_start:range_end]:
            illum_list.append(data.text.strip())
        for j in range(0, 10):
            if span_subheader_sm[j].text.strip() not in header_data:
                header_data[span_subheader_sm[j].text.strip()] = [illum_list[j]]
            else:
                header_data[span_subheader_sm[j].text.strip()].append(illum_list[j])
    
    df = pd.DataFrame.from_dict(header_data)
    df.rename(columns={'% Illumination @ 0Z': '% Illum @ 0000Z'}, inplace=True)

    return df
 

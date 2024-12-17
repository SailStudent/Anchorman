from bs4 import BeautifulSoup

def get_af_visibility(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Collecting the date data
    forecast_div = soup.find('div', id='forecast_div')
    forecast_table = forecast_div.find_all('td', class_='test2 time')
    forecast_table = [forecast.get_text(strip=True) for forecast in forecast_table]
    forecast_table = [int(forecast_table[i][:2]) for i in range(len(forecast_table))]
    
    # Collecting the visibility data
    vis_table = forecast_div.find_all('tr', class_='bottomborder outlook_row')
    vis_section = forecast_div.find_all('td', class_='test2 forecast')[17:34]
    vis_section = [float(vis.get_text(strip=True)) for vis in vis_section]

    # Calculate the average visibility for each day in the forecast
    vis_dict={}
    for i in range(len(forecast_table)):
        if forecast_table[i] in vis_dict.keys():
            vis_dict[forecast_table[i]] += vis_section[i]
            
        else:
            vis_dict[forecast_table[i]] = vis_section[i]
            
    for key in vis_dict:
        count = forecast_table.count(key)
        vis_dict[key] /= count 
        vis_dict[key] = vis_dict[key] * 1609.34 # converting to meters

        vis_condition = ""  
        
        if vis_dict[key] >= 10000:
            vis_condition = ">10k - Very Good"
        elif vis_dict[key] >= 5000:
            vis_condition = "5-10k - Good"
        elif vis_dict[key] >= 3000:
            vis_condition = "3-5k - Moderate"
        elif vis_dict[key] >= 1000:
            vis_condition = "1-3k - Poor"
        else:
            vis_condition = "0-1k - Very Poor"
    
    return vis_condition

if __name__ == '__main__':
    html_content = 'services/AFW-WEBS_Detroit.html'
    get_af_visibility(html_content)
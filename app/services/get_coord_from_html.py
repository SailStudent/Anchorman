from bs4 import BeautifulSoup

def get_coord_from_html(html_file):
    """
    This function extracts the latitude and longitude from the html file.
    :param html_file: The html file to extract the latitude and longitude from.
    :return: A tuple containing the latitude and longitude.
    """
    # with open(html_file, 'r', encoding='utf-8') as file:
    #     html = file.read()

    soup = BeautifulSoup(html_file, 'html.parser')

    test2s = soup.find_all('td', class_='test2')


    
    if test2s[0].get_text(strip=True)[:8] == 'Latitude':
        lat = test2s[0].get_text(strip=True)
        lat = float(lat.replace("Latitude: ", ""))
        lon = test2s[1].get_text(strip=True)
        lon = float(lon.replace("Longitude: ", ""))
    else:
        lat = test2s[1].get_text(strip=True)
        lat = float(lat.replace("Latitude: ", ""))
        lon = test2s[2].get_text(strip=True)
        lon = float(lon.replace("Longitude: ", ""))
   

    return lat, lon

if __name__ == '__main__':
    html_file = 'services/AFW-WEBS_Detroit.html'
    print(get_coord_from_html(html_file))


def get_location_name(html_file):
    soup = BeautifulSoup(html_file, 'html.parser')
    location_name = soup.find('span', class_='span_subheader_lg').get_text(strip=True)
    # location_name = location_name.get_text(strip=True)
    location_name = location_name.split(',')[0]
    return location_name
   
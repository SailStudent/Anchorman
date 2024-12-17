from bs4 import BeautifulSoup


def get_af_weather_html(file_input):

    with open(file_input, 'r', encoding="utf-8") as file:
        html = file.read()
    
    soup = BeautifulSoup(html, 'html.parser')  #Need to add this and refactor the other functions in order to reduce the repetative code
    
    return soup



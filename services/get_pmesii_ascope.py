# get_pmesii_ascope.py

# Standard library imports
import os
import logging
import json
import re

# Third-party library imports
import requests_pkcs12

# Configure logging for error handling
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Retrieve the password from the environment variable
LOADOUT_PASSWORD = os.environ.get("LOADOUT_PASSWORD", "bdppassword1")

def create_pmesii_ascope_crosswalk(location_of_interest_1):
    url = 'https://omni.army.mil/camogptapi/model/v1/chat/completions'
    cert_path = os.path.join(os.path.dirname(__file__), 'anchorman.p12')
    cert_password = LOADOUT_PASSWORD

    TEMPERATURE = 0.5

    FUNCTION_SYSTEM_PROMPT = (
        "You are a helpful assistant designed to output a ASCOPE/PMESII crosswalk. "
        "PMESII stands for Political, Military/Police, Economic, Social, Infrastructure, Information. "
        "ASCOPE stands for Areas, Structures, Capabilities, Organizations, People, Events. "
        "The output should be in JSON format with the following structure: "
        "{ "
        '  "ASCOPE/PMESII": { '
        '    "Areas": { '
        '      "Political": ["Bullet1", "Bullet2"], '
        '      "Military": ["Bullet1", "Bullet2", "Bullet3"], '
        '      ... '
        '    }, '
        '    "Structures": { '
        '      ... '
        '    }, '
        '    ... '
        '  } '
        "} "
        "Ensure that all keys and string values are enclosed in double quotes as required by the JSON standard. Do not use single quotes. "
        "Do not include tabs or dashes within the JSON strings. Bullets should be simple strings within the lists. "
        "Unless otherwise prompted, the default is that each sub-variable section will contain UP TO THREE BULLETS describing the "
        f"most pertinent information with reference to the two associated variables (column and row) which would affect friendly military operations in {location_of_interest_1}. "
        "Full sentences must be used when describing PMESII Capabilities. Full sentences may also be used used when additional detail is required such as when describing Areas or Organizations if additional context is needed. "
        "**IMPORTANT: Each bullet will be formatted as follows: a one to three word main point, followed by a colon, followed by a SEVEN TO TWELVE word description or longer as necessary to convey the important information. (ie: 'Main Point: Seven to Twelve word description')"
        "Ensure the response is as detailed as possible including dates along with full names of specific people, places (with eight digit Military Grid Reference System (MGRS) in parenthesis such as 38S MC 1234 5678), and organizations when available. "
        "The type of information to include in each sub-variable section is: "
        "Political:Areas - District Boundary or Party affiliation areas; "
        "Political:Structures - town halls or other major government offices; "
        "Political:Capabilities - Dispute resolution or Insurgent capabilities; "
        "Political:Organization - Political parties and other power brokers such as the United Nations; "
        "Political:People - Governors, councils or elders; "
        "Political:Events - elections or council meetings; "
        "Military:Areas - Key host nation military bases, U.S. or other FVEY (ie: UK, New Zealand, Australia, Canada) partner nation bases/presence, historic combat sites, or any other key military locations that are not physical structures; "
        "Military:Structures - Military/Police headquarters locations, major missile sites, lines of defense, or any other key military structures; "
        "Military:Capabilities - host nation military or police security posture, host nation military's strengths and weaknesses; "
        "Military:Organizations - different units in the military/police, insurgent groups present at the location, or other key militant power brokers; "
        "Military:People - key host nation military leaders, key leaders from FVEY partner militaries, or key leaders from insurgent groups; "
        "Military:Events - lethal/nonlethal events, loss of military leadership, loss of insurgent leadership, major military operations or attacks, or any major military anniversary; "
        "Economic:Areas - bazaars, shops, markets, or any other significant areas that effect the local, regional, or global economy; "
        "Economic:Structures - banks, markets, storage facilities, logistics hubs, or other major economic facilities; "
        "Economic:Capabilities - access to banks, economy's ability to withstand natural disasters, agriculture capabilities, or major imports/exports; "
        "Economic:Organizations - banks, large land holders, big businesses, or any other organizations that effect the local, regional, or global economy; "
        "Economic:People - key bankers, landholders, or merchants in the area; "
        "Economic:Events - drought, harvest, or business open/close times; "
        "Social:Areas - parks and other major meeting areas; "
        "Social:Structures - churches, restaurants, bars, etc.; "
        "Social:Capabilities - strength of local & national ties; "
        "Social:Organizations - tribes, clans, families, youth groups, non-government organizations, or international government organizations; "
        "Social:People - religious leaders or influential families; "
        "Social:Events - holidays, weddings, or notable religious days; "
        "Information:Areas - key locations of different radio, TV, and newspaper outlets, or other areas where people gather for word-of-mouth; "
        "Information:Structures - specific radio, television, cellular network, or internet service providers along with the specific locations where the services are provided; "
        "Information:Capabilities - literacy rate, availability of media (television/radio/state ran media) and where it's available, and the availability of cellular networks and internet service providers and which types are available (ie: LTE 5G, Fiberoptic, etc.); "
        "Information:Organizations - news groups, influential people who pass word, internet service providers, telecoms companies, etc.; "
        "Information:People - Media owners, Mullahs, or heads of powerful families; "
        "Information:Events - Information Operation (IO) campaigns, project openings, civilian casualty events; "
        "Infrastructure:Areas - irrigation networks, water tables, medical coverage, etc.; "
        "Infrastructure:Structures - key roads, bridges, power lines, walls, dams, etc.; "
        "Infrastructure:Capabilities - Ability to build / maintain roads, walls, dams, etc.; "
        "Infrastructure:Organizations - Government ministries, construction companies, etc.; "
        "Infrastructure:People - Builders, contractors, or development councils; "
        "Infrastructure:Events - road / bridge construction, well digging, scheduled maintenance, etc. "
        "IMPORTANT: DO NOT INCLUDE ANY ADDITIONAL TEXT BESIDES THE JSON AND THE REFERENCES. NO ADDITIONAL TEXT OR CLARIFICATION, JUST THE JSON AND REFERENCES. "
        "This is very important because the JSON will be parsed into a table where the PMESII variables become column headers and the ASCOPE variables become row headers with the appropriate information inside of each cell. "
        "Within each sub-variable section there should be up to two bullets. Each individual bullet should include a reference number(s) in square brackets (e.g., [1] or [2,3]) at the end of the bullet, depending on where that bullet was sourced from. "
        "IMPORTANT: After the JSON output, and before the reference information, you MUST include a line with exactly 'xxxxxxxxxx'. This line is crucial and will be used for parsing purposes. "
        "Ensure to include a list of references below the PMESII/ASCOPE crosswalk information after the 'xxxxxxxxxx' line with the associated URL. DO NOT use Wikipedia as a soure. "
        "The references should be an ordered list with each new source on a new line. "
        "DO NOT INCLUDE ANYTHING OTHER THAN THE JSON AND THE REFERENCES. "
    )

    USER_PROMPT = (
        f"Generate a PMESII/ASCOPE crosswalk for {location_of_interest_1} in JSON format as described where each sub-variable section contains information specific to {location_of_interest_1}. "
        "Unless otherwise prompted, the DEFAULT IS THAT EACH SUB-VARIABLE SECTION WILL CONTAIN THREE TO FOUR BULLETS and will contain detailed information that describes the importance of the information in those bullets. "
        "Each ASCOPE category ('Areas', 'Structures', 'Capabilities', 'Organizations', 'People', 'Events') should contain the PMESII variables as keys, with values being lists of bullet points. "
        "Ensure all keys and strings are enclosed in double quotes. Do not include tabs, dashes, or any formatting characters within the JSON strings. "
        "IMPORTANT: EACH BULLET WILL CONTAIN A TWO TO THREE WORD MAIN POINT FOLLOWED BY A SEVEN TO TWELVE WORD DESCRIPTION OR LONGER AS NEEDED TO CONVEY THE NECESSARY IMPORTANT INFORMATION such as names of districts, names and goals of political parties, key military capabilities in depth, key military/insurgent organizations and their structure, etc. "
        "IMPORTANT: BE AS DETAILED AS POSSIBLE, BUT KEEP THE RESPONSE CONCISE due to rate limiting. " 
        "IMPORTANT: USE SPECIFIC FULL NAMES OF PEOPLE (including aliases), ORGANIZATIONS AND THE PEOPLE WHO LEAD THOSE ORGANIZATIONS, LOCATIONS (including Military Grid Reference System coordinates), BUILDINGS with MGRS grid coordinates, and SPECIFIC MILITARY EQUIPMENT at given locations when available. "
    )

    try:
        # Prepare the data for the AI assistant
        question_data = {
            "model": "Mistral7B",
            "messages": [
                {"role": "system", "content": FUNCTION_SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT},
            ],
            "temperature": TEMPERATURE
        }

        chat_response = requests_pkcs12.post(
            url,
            json=question_data,
            headers={'Content-Type': 'application/json'},
            pkcs12_filename=cert_path,
            pkcs12_password=cert_password,
            verify=False
        )

        if chat_response.status_code != 200:
            raise ValueError(f"Chat API request failed with status code: {chat_response.status_code}")

        # Process the response
        response_json = chat_response.json()
        response_text = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")

        if not response_text:
            raise ValueError("No content returned from the LLM response")

        # Parse response_text to create a DataFrame and references
        data, references = parse_response_to_dataframe(response_text)
        return data, references

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return None, str(e)

def parse_response_to_dataframe(response_text):
    # Split response into JSON data and references using 'xxxxxxxxxx'
    parts = response_text.strip().split('xxxxxxxxxx')
    if len(parts) < 2:
        raise ValueError("Response text does not contain the 'xxxxxxxxxx' separator.")
    json_text = parts[0].strip()
    references_text = parts[1].strip()

    # Remove code block markers and optional 'json' specifier
    json_text = re.sub(r'^```(?:json)?\n?', '', json_text)
    json_text = re.sub(r'\n?```$', '', json_text)

    try:
        # Parse the JSON data
        data = json.loads(json_text)
        return data, references_text
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON data: {e}")
        return None, references_text

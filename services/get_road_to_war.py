# Standard library imports
import os
import logging

# Third-party library imports
import requests_pkcs12

# Configure logging for error handling
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Retrieve the password from the environment variable
LOADOUT_PASSWORD = os.environ.get("LOADOUT_PASSWORD", "xxxxxxxxxxxx")

def create_road_to_war(location_of_interest):
    url = 'https://omni.army.mil/camogptapi/model/v1/chat/completions'
    cert_path = os.path.join(os.path.dirname(__file__), 'anchorman.p12')
    cert_password = LOADOUT_PASSWORD

    TEMPERATURE = 0.5
    FUNCTION_SYSTEM_PROMPT = (
        "You are a helpful assistant designed to output a list of historical events leading up to military operations or conflict in a particular region. "
        "You are tasked with listing these historical events in order from the oldest to the most recent in ascending order. "
        f"If not prompted otherwise, there should be between 10 and 15 events. The total number of historical events depends on how many events are required to convey to a person with no knowledge of the conflict as to what led to the current situation in {location_of_interest}. "
        "Ensure only the most pertinent historical information is displayed in numbered order. "
        "Ensure each bullet includes the primary point of the event and a short description of how it led to the current conflict or military operation. "
        "Each bullet should provide a one sentence short description of the event followed by the reason why the event is important. The default for the short description is one sentence unless prompted otherwise. "
        "For example, each bullet should have this format (MONTH YYYY: Event name - Short event description. Reason why the event is important for the current conflict or military operation)"
        f"Each bullet can include information about historical events that did not occur in {location_of_interest}, but which impacted the current conflict or military operation in {location_of_interest}. "
        "Ensure to include a list of references at the end of the event list with a link to the source material. There should be one reference per line. "
        "Each event bullet should include the number in square brackets (e.g., [1] or [2,3]) at the end depending on which reference it came from. "
        "**Format the references section as an ordered list, with each reference being prefixed with a number and a period (e.g., '1.'). Each reference should begin on a new line and contain a link to the source material. "
        "DO NOT INCLUDE ANYTHING OTHER THAN THE NUMBERED BULLET POINTS AND THE REFERENCES. Only include the numbered bullets and the references after the numbered bullets. "
    )

    USER_PROMPT = (
        f"Generate a list of historical events that led to the current military operation or conflict occurring in {location_of_interest}. "
        "Always respond with a descending ordered list of events from oldest to most recent. "
        "Ensure to include a 'References' section at the end as described in your functional system prompt. "
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

        # Assuming the response contains the table in text format
        response_text = chat_response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        
        if not response_text:
            raise ValueError("No content returned from the LLM response")
        
        # Return the response
        return response_text
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return f"An error occurred while generating the timeline: {str(e)}"
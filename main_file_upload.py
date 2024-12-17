# main_file_upload.py

# Standard library imports
import os

# Third-party library imports
import streamlit as st
from pptx import Presentation
import pandas as pd
import markdown

# Local library imports
from services.get_coord_from_html import get_coord_from_html, get_location_name
from helpers_af.create_af_powerpoint import create_af_powerpoint
from helpers_af.create_powerpoint_single_city import create_powerpoint_single_city
from helpers_af.create_af_illum_dataframe import create_af_illum_dataframe
from helpers_af.get_af_visibility import get_af_visibility
from helpers_af.map_scale_dictionary import zoom_mapping, zoom_options
from styles.css_styles import hide_streamlit_style, custom_css
from services.get_pmesii_ascope import create_pmesii_ascope_crosswalk
from services.get_road_to_war import create_road_to_war

# Initialize session state variables for PMESII/ASCOPE
if 'pmesii_df' not in st.session_state:
    st.session_state.pmesii_df = None
if 'pmesii_references' not in st.session_state:
    st.session_state.pmesii_references = None

# Ensure the output directory exists
os.makedirs(".output/", exist_ok=True)

# Set up the page configuration as the first Streamlit command
st.set_page_config(
    page_title='Anchorman',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Apply CSS styling
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("<h1 style='color:black; text-align: left; font-size:40px; font-weight:bold;'>Anchorman</h1>", unsafe_allow_html=True)
    st.sidebar.image('static/anchorman/AI2C.png', width=120)

    # Create radio buttons for main sections
    main_section = st.radio("Select Section", ["Weather", "Road to War", "PMESII/ASCOPE"])

    # Help guide button with a unique key
    how_to_button = st.button("Weather How to Guide", key="how_to_guide_button")

    # PMESII/ASCOPE example button with a unique key
    pmesii_ascope_examples_button = st.button("PMESII/ASCOPE Examples", key="pmesii_ascope_examples_button")

    # Lock the feedback button to the bottom of the sidebar
    feedback_button = st.button("Found a bug or have feedback?", key="feedback_button")

    # Placeholder for success message and gif
    success_placeholder = st.empty()
    
# PMESII/ASCOPE examples for how to use the additional requirements input box
if pmesii_ascope_examples_button:
    @st.dialog("Additional requirement examples")
    def pmesii_ascope_examples_button():
        st.markdown("Example 1. ENSURE EACH SECTION CONTAINS A TOTAL OF FOUR TO FIVE BULLETS. THIS IS EXTREMELY IMPORTANT.")
        st.markdown("Example 2. USE ONLY REFERENCES FROM ACADEMIC RESEARCH.")
        st.markdown("Example 3. REFERENCE ONLY OFFICIAL GOVERNMENT SOURCES.")
        st.markdown("WARNING: Only request changes to data content. DO NOT attempt to alter the output format.")
        st.markdown("Type your additional requirement in CAPS to convey importance.")
        st.markdown("Stay Classy!")
    # Call the function to display the dialog
    pmesii_ascope_examples_button()

# Help box for how to use the application
if feedback_button:
    @st.dialog("Found a bug or have feedback?")
    def feedback_butt():
        st.markdown("Send an email to both of:")
        st.markdown("michael.belyayev.mil@socom.mil")
        st.markdown("zachary.c.murphy.mil@socom.mil")
        st.markdown("Please include a detailed description of the issue or feedback.")
        st.markdown("Copy and paste our emails; they will not link directly.")
    feedback_butt()

# Help box for how to use the application
if how_to_button:
    @st.dialog("How to use Anchorman Weather")
    def how_to_guide():
        st.markdown("1. Navigate to [weather.af.mil](https://weather.af.mil) and log in.")
        st.markdown("2. Scroll to the bottom of the page and click 'Local Weather'.")
        st.markdown("3. Enter the desired city in the search bar.")
        st.markdown("4. Click the specific location (if more than one is displayed).")
        st.markdown("5. Allow the page to completely load.")
        st.markdown("6. Right-click on the page and select 'Save As'.")
        st.markdown("7. Save the file as an HTML file (Webpage, complete).")
        st.markdown("8. You can now upload that file to Anchorman.")
        st.markdown("9. Select the desired map scale.")
        st.markdown("10. Enter the desired operation length in days.")
        st.markdown("11. Click the 'Generate Slide' button.")
        st.markdown("12. Download the slide by clicking the download button.")
        st.markdown("13. Stay Classy!")
    # Call the function to display the dialog
    how_to_guide()

# Create main content area starting on Weather section
if main_section == "Weather":
    # Create tabs for "Single Location" and "Multiple Locations"
    tab_single, tab_multi = st.tabs(["Single Location", "Multiple Locations"])

    with tab_single:
        st.header("Single Location Weather Forecast")
        # Upload HTML file for single city
        location1_html = st.file_uploader("Upload HTML file for single city", type=["html"], accept_multiple_files=False)
        try:
            if location1_html is None:
                location1_html_from_af = ""
            else:
                location1_html_from_af = location1_html.read().decode('utf-8')
                location1_name = get_location_name(location1_html_from_af)
        except TypeError:
            location1_html_from_af = ""

        # Map scale selection
        selected_scale = st.selectbox("Select map scale (default 1:500k):", options=zoom_options, index=11)
        zoom_level = zoom_mapping[selected_scale]

        # Start day and operation length
        start_day = int(st.text_input("Enter start day (1-5):", value="1"))
        num_days = int(st.text_input("Enter operation length in days:", value="1"))

        if st.button("Generate Weather Slide"):
            success = False
            location1_coords = get_coord_from_html(location1_html_from_af)
            if location1_coords:
                location1_lat, location1_lon = location1_coords
                location1_illum_df = create_af_illum_dataframe(location1_html_from_af)
                location1_vis_condition = get_af_visibility(location1_html_from_af)

                create_powerpoint_single_city(
                    location1_name,
                    location1_html_from_af,
                    location1_illum_df,
                    location1_vis_condition,
                    location1_lat, location1_lon,
                    start_day,  # Pass the start day
                    num_days,   # Pass the operation length
                    zoom_level
                )
                success = True
            else:
                st.error("Could not retrieve coordinates for the specified location.")

            if success:
                st.markdown("<div class='stSuccess'>I don't know how to put this, but I'm kind of a big deal!</div>", unsafe_allow_html=True)
                # Update the success_placeholder in the sidebar with gif
                with success_placeholder:
                    st.markdown("<div class='stSuccess'>I don't know how to put this, but I'm kind of a big deal!</div>", unsafe_allow_html=True)
                    st.image("static/anchorman/yay.gif", use_column_width=True)
                try:
                    with open(".output/Weather_Forecast.pptx", "rb") as file:
                        st.download_button(
                            label="Download Weather Slide",
                            data=file,
                            file_name="Weather_Forecast.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            key='download_weather_slide_single'  # Assign a unique key
                        )
                except FileNotFoundError:
                    st.error("Failed to create the PowerPoint file.")

    with tab_multi:
        st.header("Multiple Locations Weather Forecast")
        # Upload HTML files for two cities
        location1_html = st.file_uploader("Upload HTML file for the first city", type=["html"], accept_multiple_files=False, key="multi_loc1")
        try:
            if location1_html is None:
                location1_html_from_af = ""
            else:
                location1_html_from_af = location1_html.read().decode('utf-8')
                location1_name = get_location_name(location1_html_from_af)
        except TypeError:
            location1_html_from_af = ""

        location2_html = st.file_uploader("Upload HTML file for the second city", type=["html"], accept_multiple_files=False, key="multi_loc2")
        try:
            if location2_html is None:
                location2_html_from_af = ""
            else:
                location2_html_from_af = location2_html.read().decode('utf-8')
                location2_name = get_location_name(location2_html_from_af)
        except TypeError:
            location2_html_from_af = ""

        # Map scale selection
        selected_scale = st.selectbox("Select map scale (default 1:500k):", options=zoom_options, index=11, key="multi_scale")
        zoom_level = zoom_mapping[selected_scale]

        # Start day and operation length
        start_day = int(st.text_input("Enter start day (1-5):", value="1", key="multi_start_day"))
        num_days = int(st.text_input("Enter operation length in days:", value="1", key="multi_num_days"))

        if st.button("Generate Weather Slide", key="multi_generate"):
            success = False
            location1_coords = get_coord_from_html(location1_html_from_af)
            location2_coords = get_coord_from_html(location2_html_from_af)

            if location1_coords and location2_coords:
                location1_lat, location1_lon = location1_coords
                location2_lat, location2_lon = location2_coords
                location1_illum_df = create_af_illum_dataframe(location1_html_from_af)
                location1_vis_condition = get_af_visibility(location1_html_from_af)
                location2_illum_df = create_af_illum_dataframe(location2_html_from_af)
                location2_vis_condition = get_af_visibility(location2_html_from_af)

                prs = Presentation()
                create_af_powerpoint(
                    prs,
                    location1_name,
                    location2_name,
                    location1_html_from_af,
                    location2_html_from_af,
                    location1_illum_df,
                    location2_illum_df,
                    location1_vis_condition,
                    location2_vis_condition,
                    location1_lat, location1_lon,
                    location2_lat, location2_lon,
                    start_day,
                    num_days
                )
                success = True
            else:
                st.error("Could not retrieve coordinates for one or both specified locations.")

            if success:
                st.markdown("<div class='stSuccess'>I don't know how to put this, but I'm kind of a big deal!</div>", unsafe_allow_html=True)
                # Update the success_placeholder in the sidebar with gif
                with success_placeholder:
                    st.markdown("<div class='stSuccess'>I don't know how to put this, but I'm kind of a big deal!</div>", unsafe_allow_html=True)
                    st.image("static/anchorman/yay.gif", use_column_width=True)
                try:
                    with open(".output/Weather_Forecast.pptx", "rb") as file:
                        st.download_button(
                            label="Download Weather Slide",
                            data=file,
                            file_name="Weather_Forecast.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            key='download_weather_slide_multiple'  # Assign a unique key
                        )
                except FileNotFoundError:
                    st.error("Failed to create the PowerPoint file.")

# Create Road to War section
elif main_section == "Road to War":
    st.header("Road to War")
    # Location of interest input
    location_of_interest = st.text_input("Enter Location of Interest (City, Province, Country)", value="ex: Beirut, Lebanon")
    
    # User input box for additional information
    generic_prompt_add= "**IMPORTANT - THE FOLLOWING STATEMENTS SHOULD OVERRIDE PREVIOUS REQUIREMENTS: "
    show_text_area = st.checkbox("Add additional requirements")
    user_input=""
    if show_text_area:
        user_input = st.text_area("Add additional requirements below", value="")

    if user_input != "":
        user_input = generic_prompt_add + user_input

    st.write(
        "WARNING: Adding additional requirements may have unintended negative effects "
        "on the output of this product. Be as precise as possible and do not attempt to "
        "alter the output format (i.e., table format with references). See examples button to the left."
    )

    if st.button("Generate Road to War"):
        with st.spinner("Generating Road to War... This may take a moment."):
            full_location_prompt = f"{location_of_interest}. {user_input}"
            
            timeline = create_road_to_war(full_location_prompt)  # Use the combined prompt

            # Check if timeline is a dictionary with an error
            if isinstance(timeline, dict) and "error" in timeline:
                st.error(f"Error: {timeline['error']}")
            else:
                # Convert Markdown to HTML
                timeline_html = markdown.markdown(timeline)
                st.markdown(f"<div class='road-to-war-output'>{timeline_html}</div>", unsafe_allow_html=True)

# Create PMESII/ASCOPE section
elif main_section == "PMESII/ASCOPE":
    st.header("PMESII/ASCOPE Crosswalk")
    location_of_interest_1 = st.text_input(
        "Enter Location of Interest (City, Province, Country)",
        value="ex: Hudaydah, Yemen"
    )

    # User input box for additional information
    generic_prompt_add= "**IMPORTANT - THE FOLLOWING STATEMENTS SHOULD OVERRIDE PREVIOUS REQUIREMENTS: "
    show_text_area = st.checkbox("Add additional requirements")
    user_input=""
    if show_text_area:
        user_input = st.text_area("Add additional requirements below", value="")

    if user_input != "":
        user_input = generic_prompt_add + user_input

    st.write(
        "WARNING: Adding additional requirements may have unintended negative effects "
        "on the output of this product. Be as precise as possible and do not attempt to "
        "alter the output format (i.e., table format with references). See examples button to the left."
    )

    if st.button("Generate PMESII/ASCOPE Crosswalk"):
        with st.spinner("Generating PMESII/ASCOPE Crosswalk... This may take a moment."):
            # Append user input to the prompt
            full_location_prompt = f"{location_of_interest_1}. {user_input}"
            
            data, references = create_pmesii_ascope_crosswalk(full_location_prompt)

            if data is not None:
                # Store the JSON data and references in session state
                st.session_state.pmesii_data = data
                st.session_state.pmesii_references = references
            else:
                st.error(
                    "Failed to retrieve PMESII/ASCOPE Crosswalk. "
                    "Please check the logs for more details."
                )
                st.session_state.pmesii_data = None
                st.session_state.pmesii_references = None

    # Check if data exists in session state and display it
    if st.session_state.get('pmesii_data') is not None:
        data = st.session_state.pmesii_data
        references = st.session_state.pmesii_references

        # Define the ASCOPE and PMESII categories
        ascope_categories = ["Areas", "Structures", "Capabilities", "Organizations", "People", "Events"]
        pmesii_categories = ["Political", "Military", "Economic", "Social", "Information", "Infrastructure"]

        # Create an empty DataFrame with ASCOPE categories as index and PMESII categories as columns
        df = pd.DataFrame(index=ascope_categories, columns=pmesii_categories)

        # Fill the DataFrame with data from JSON
        for ascope_key in ascope_categories:
            pmesii_values = data.get("ASCOPE/PMESII", {}).get(ascope_key, {})
            for pmesii_key in pmesii_categories:
                bullets = pmesii_values.get(pmesii_key, [])
                if bullets:
                    # Join the bullets into a single string separated by newlines
                    df.at[ascope_key, pmesii_key] = '\n'.join(bullets)
                else:
                    df.at[ascope_key, pmesii_key] = ""

        # Display the data using expanders for each PMESII variable
        for pmesii_key in pmesii_categories:
            with st.expander(pmesii_key):
                for ascope_key in ascope_categories:
                    bullets_str = df.at[ascope_key, pmesii_key]
                    if bullets_str:
                        st.write(f"**{ascope_key}:**")
                        bullets_list = bullets_str.split('\n')
                        # Format bullets with dashes
                        content_str = '\n'.join([f"- {bullet}" for bullet in bullets_list])
                        st.markdown(content_str)
                    else:
                        st.write(f"**{ascope_key}:** No data available.")

        # Display the references
        st.markdown("### References")
        references_html = markdown.markdown(references)
        st.markdown(f"<div class='pmesii-output'>{references_html}</div>", unsafe_allow_html=True)

        # Provide an option to download the DataFrame as a CSV file
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download PMESII/ASCOPE Crosswalk as CSV",
            data=csv,
            file_name='pmesii_ascope_crosswalk.csv',
            mime='text/csv',
            key='download_pmesii_ascope_csv'
        )
        
# Add the classification banner
st.markdown("<div id='classification-banner'>CONTROLLED UNCLASSIFIED INFORMATION</div>", unsafe_allow_html=True)

# Add the warning banner
st.markdown("<div id='warning-banner'>Experimental - Non-Production System Approved for IL5 CUI Data (TRL 4)</div>", unsafe_allow_html=True)

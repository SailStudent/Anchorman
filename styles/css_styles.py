# css_styles.py

hide_streamlit_style = """
<style>
/* Hide the Streamlit menu, footer, and header */
#MainMenu {visibility: hidden;}  /* Hide the hamburger menu */
footer {visibility: hidden;}     /* Hide the footer */
header {visibility: hidden;}     /* Hide the header */
<style>

/* Hide the Streamlit menu, footer, and header */
#MainMenu {visibility: hidden;}  /* Hide the hamburger menu */
footer {visibility: hidden;}     /* Hide the footer */
header {visibility: hidden;}     /* Hide the header */

/* Set the body margin and padding to 0 */
body {
    margin: 0 !important;
    padding: 0 !important;
}
/* Set the body margin and padding to 0 */
body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove padding at the top of the block container */
.block-container {
    padding-top: 0 !important;
    padding-bottom: 1rem !important;
    margin-top: 0px !important;
}

/* Remove padding from the main content area */
.main {
    padding: 0 !important;
    margin: 0 !important;
}

/* Remove padding from the main content area */
.main {
    padding: 0 !important;
    margin: 0 !important;
}
</style>
"""

custom_css = """
<style>

/* Classification banner at the bottom */
#classification-banner {
    background-color: rgb(18, 122, 32);
    color: white;
    text-align: center;
    font-weight: bold;
    font-size: 14px;
    padding: 1px 0;
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100vw;
    z-index: 100;
}

/* Warning banner at the top */
#warning-banner {
    background-color: rgb(255, 0, 0);
    color: white;
    text-align: center;
    font-weight: bold;
    font-size: 14px;
    padding: 5px 0;
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    z-index: 1000;
}

/* Sidebar background color */
[data-testid="stSidebar"] {
    color: black !important;
    background-color: gray !important;
}

/* Font size and alignment for the "Anchorman" title at the very top of the sidebar */
h1 {
    margin-top: -30px !important;
    padding-top: 0 !important;
    font-size: 48px;
}

/* Ensure all text inside the sidebar is size 18 */
[data-testid="stSidebar"] * {
    font-size: 18px;
}

/* Ensure specific text elements inside the sidebar are yellow, excluding those inside buttons */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] h5,
[data-testid="stSidebar"] h6,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p:not(:is(button p, button p *)),
[data-testid="stSidebar"] span:not(:is(button span, button span *)) {
    color: rgb(194, 194, 23) !important;
}

/* Style buttons in the sidebar */
[data-testid="stSidebar"] [data-testid="stButton"] button {
    background-color: rgb(194, 194, 23) !important;
    color: white !important;
    border-color: rgb(194, 194, 23) !important;
    border-radius: 15px !important;
    margin: 4px 0 !important;
    padding: 8px 16px !important;
    font-size: 18px !important;
}

/* Button styles for tabs in main content */
div[data-testid="stTabs"] button {
    background-color: rgb(194, 194, 23);
    color: white !important;
    border-color: rgb(194, 194, 23);
    border-radius: 15px !important;
    margin-right: 4px !important;
    padding: 8px 16px !important;
    font-size: 18px !important;
}

div[data-testid="stTabs"] button:hover {
    background-color: #f1d060;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    background-color: rgb(194, 194, 23);
    color: white !important;
    border-color: rgb(194, 194, 23);
    border-radius: 15px 15px 0 0 !important;
    font-size: 18px !important;
}

/* Styling for success messages */
.stSuccess {
    font-size: 24px !important;
    font-weight: bold !important;
    color: green !important;
    background-color: transparent !important;
    padding: 0 !important;
    border: none !important;
}

/* Main content area text should be white and 18px */
/* Main content area text should be white and 18px */
body, .main, div[data-testid="stAppViewContainer"] .block-container p {
    color: white !important;
    font-size: 18px !important;
}

/* Ensures the Anchorman title is size 40px */
h1{
    font-size: 40px !important;
}

/* Ensures the top heading element on the main page has yellow text and size 24px */
h2 {
    color: rgb(194, 194, 23) !important;
    font-size: 24px !important;
}

/* Ensure input boxes and their labels are styled properly */
input[type="text"], textarea, select {
    background-color: white !important;
    color: black !important;
    font-size: 18px !important;
}

/* Ensure the label text remains white */
label {
    color: white !important;
}

/* Sidebar text and form elements should remain size 18px */
input, textarea, select, label {
    font-size: 18px !important;
}

body {
    background-color: black;
}

.stApp {
    background-color: black;
    color: white !important;
}

/* Style for the Road to War output */
.road-to-war-output {
    color: white !important;
    line-height: 1.5;
}

.road-to-war-output ul, .road-to-war-output ol {
    margin-left: 20px;
    font-size: 16px !important;
}

.road-to-war-output li {
    margin-bottom: 8px;
    font-size: 16px !important;
}

/* Style for the PMESII/ASCOPE output */
.pmesii-output {
    color: white !important;
    line-height: 1.5;
}

.pmesii-output ul {
    margin-left: 20px;
    font-size: 16px !important;
    list-style-type: disc;  /* Bullets for unordered lists */
}

.pmesii-output ol {
    margin-left: 20px;
    font-size: 16px !important;
    list-style-type: decimal;  /* Numbers for ordered lists */
}

.pmesii-output li {
    margin-bottom: 8px;
    font-size: 16px !important;
}

/* Ensure that unordered lists use circle bullets */
.pmesii-output ul {
    list-style-type: circle;
}

div[data-testid="stAppViewContainer"] .stButton button,
div[data-testid="stAppViewContainer"] .stDownloadButton button {
    background-color: rgb(194, 194, 23) !important;
    color: white !important;
    border-color: rgb(194, 194, 23) !important;
    border-radius: 15px !important;
    margin: 4px !important;
    padding: 8px 16px !important;
    font-size: 18px !important;
}

</style>
"""

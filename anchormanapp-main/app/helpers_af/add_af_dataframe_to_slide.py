from pptx.enum.text import MSO_VERTICAL_ANCHOR
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from helpers_af.add_dataframe_to_slide import add_dataframe_to_slide_single_city

def add_af_dataframe_to_slide(prs, slide, location1_forecast_df, location2_forecast_df, location1_illum_df, location2_illum_df):
    # Align tables properly
    table1_left = Inches(0)
    table2_left = int(prs.slide_width / 2)
    table_top = Inches(3.8)
    table_width = int(prs.slide_width / 2)
    table_height = Inches(2.3)

    table1, _= add_dataframe_to_slide_single_city(location1_forecast_df, location1_illum_df, slide, table1_left, table_top, table_width, table_height, dual_city=False)
    table2, _ = add_dataframe_to_slide_single_city(location2_forecast_df, location2_illum_df, slide, table2_left, table_top, table_width, table_height, dual_city=False)

    

    # Adding illumination tables
    illum_table_top = Inches(6.1)
    illum_table_height = Inches(1.4)
    _, table1_illum =  add_dataframe_to_slide_single_city(location1_forecast_df, location1_illum_df, slide, table1_left, illum_table_top, table_width, illum_table_height, dual_city=True)
    _, table2_illum = add_dataframe_to_slide_single_city(location2_forecast_df, location2_illum_df, slide, table2_left, illum_table_top, table_width, illum_table_height, dual_city=True)
    

    return table1, table2, table1_illum, table2_illum

import pandas as pd

def get_af_atmospherics(forecast_df, illum_df, vis_condition):
    # forecast_data = pd.DataFrame({
    #     "Full Forecast": [(row["Forecast"] + " - " + row["Details"]).lower() for _, row in forecast_df.iterrows()]
    # }).head(2)
    forecast_data = {"Full Forecast": [(row["Forecast"] + " - " + row["Details"]).lower() for _, row in forecast_df.iterrows()]}
    
    AtmosphericConditions = {
        "Forecast": "",
        "Cloud Cover": "",
        "ISR Visibility": "",
        "Illum": "",
        "RW Operations": "",
        "Fog": ""
    }

    # Extract the illumination value for the first day from the illumination dataframe
    illum_value = illum_df.loc[0, '% Illum @ 0000Z']
    if float(illum_value[:-1]) > 50.0:
        AtmosphericConditions["Illum"] = ">50% - Favorable"
    else:
        AtmosphericConditions["Illum"] = "<50% - Unfavorable"

    # Set ISR visibility value in dictionary
    AtmosphericConditions["ISR Visibility"] = vis_condition
    for i in range(len(forecast_data["Full Forecast"])):
        # Determine and add forecast conditions
        if "cloudy" in forecast_data["Full Forecast"][i] and "thunder" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Cloudy w/ T-Storms"
            AtmosphericConditions["Cloud Cover"] = "Unfavorable"
            AtmosphericConditions["RW Operations"] = "Unfavorable"
            AtmosphericConditions["Fog"] = "Unfavorable"
        elif "cloudy" in forecast_data["Full Forecast"][i] and "showers" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Cloudy w/ Rain"
            AtmosphericConditions["Cloud Cover"] = "Unfavorable"
            AtmosphericConditions["RW Operations"] = "Unfavorable"
            AtmosphericConditions["Fog"] = "Unfavorable"
        elif "cloudy" in forecast_data["Full Forecast"][i] and "partly" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Partly Cloudy"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        elif "cloudy" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Cloudy"
            AtmosphericConditions["Cloud Cover"] = "Unfavorable"
            AtmosphericConditions["RW Operations"] = "Unfavorable"
            AtmosphericConditions["Fog"] = "Unfavorable"
        elif "fog" in forecast_data["Full Forecast"][i] and "sunny" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Partly Sunny"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"        
        elif "fog" in forecast_data["Full Forecast"][i] or "haze" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Hazy"
            AtmosphericConditions["Cloud Cover"] = "Unfavorable"
            AtmosphericConditions["RW Operations"] = "Unfavorable"
            AtmosphericConditions["Fog"] = "Unfavorable"
        elif "chance" in forecast_data["Full Forecast"][i] and "showers" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Chance of Rain"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        elif "shower" in forecast_data["Full Forecast"][i] and "thunder" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Cloudy w/ T-Storms"
            AtmosphericConditions["Cloud Cover"] = "Unfavorable"
            AtmosphericConditions["RW Operations"] = "Unfavorable"
            AtmosphericConditions["Fog"] = "Unfavorable"
        elif "sunny" in forecast_data["Full Forecast"][i] and "showers" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Mostly Sunny w/ Rain"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        elif "showers" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Rain"
            AtmosphericConditions["Cloud Cover"] = "Unfavorable"
            AtmosphericConditions["RW Operations"] = "Unfavorable"
            AtmosphericConditions["Fog"] = "Unfavorable"
        elif "partly sunny" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Partly Sunny"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        elif "mostly sunny" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Mostly Sunny"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        elif "sunny" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Sunny"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        elif "clear" in forecast_data["Full Forecast"][i]:
            AtmosphericConditions["Forecast"] = "Sunny"
            AtmosphericConditions["Cloud Cover"] = "Favorable"
            AtmosphericConditions["RW Operations"] = "Favorable"
            AtmosphericConditions["Fog"] = "Favorable"
        else:
            AtmosphericConditions["Forecast"] = "?????"
            AtmosphericConditions["Cloud Cover"] = "?????"
            AtmosphericConditions["RW Operations"] = "?????"
            AtmosphericConditions["Fog"] = "?????"
        
    return AtmosphericConditions

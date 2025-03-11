import pandas as pd
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

def calculate_player_form(input_path, output_path):
    player_data = pd.read_csv(input_path)

    # sort by Player_Name and Year
    player_data.sort_values(by=["Player_Name", "Year"], inplace=True)

    # calculate rolling average of runs scored (last 5 matches)
    player_data
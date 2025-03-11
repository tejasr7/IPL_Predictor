import pandas as pd
import os

# GEt the directory of the current file
script_dir = os.path.dirname(os.path.abspath(__file__))

def preprocess_player_data(input_path, output_path):
    # Load player performance data
    player_data = pd.read_csv(input_path)

    
    # handle missing values
    player_data.fillna(0, inplace=True)

    # Standardize player names
    player_data['Player_Name'] = player_data['Player_Name'].str.strip().str.title()

    # add Player_Id column
    player_data['Player_ID'] = player_data['Player_Name'].astype('category').cat.codes

    # save cleaned data
    player_data.to_csv(output_path, index=False)


if __name__ == '__main__':
    #input_path = "../data/raw/player_performance.csv"
    input_path = os.path.join(script_dir, "../../data/raw/player_performance.csv")
    output_path = os.path.join(script_dir, "../../data/processed/cleaned_player_performance.csv")

    #output_path = "../data/processed/cleaned_player_performace.csv"
    preprocess_player_data(input_path, output_path)


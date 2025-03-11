import pandas as pd
import os

def calculate_player_form(input_path, output_path):
    try:
        # Load the data
        player_data = pd.read_csv(input_path)

        # Ensure "Runs_Scored" is numeric
        player_data["Runs_Scored"] = pd.to_numeric(player_data["Runs_Scored"], errors="coerce")

        # Handle missing values (e.g., fill with 0)
        player_data["Runs_Scored"].fillna(0, inplace=True)

        # Sort by Player_Name and Year
        player_data.sort_values(by=["Player_Name", "Year"], inplace=True)

        # Calculate rolling average of runs scored (last 5 matches)
        player_data["Runs_Form"] = player_data.groupby("Player_Name")["Runs_Scored"].transform(
            lambda x: x.rolling(window=5, min_periods=1).mean()
        )

        # Save updated data
        player_data.to_csv(output_path, index=False)
        print(f"Data successfully saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {input_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define input and output paths
    input_path = os.path.join(script_dir, "../../data/processed/cleaned_player_performance.csv")
    output_path = os.path.join(script_dir, "../../data/processed/player_form.csv")

    # Run the function
    calculate_player_form(input_path, output_path)

# import pandas as pd
# import os

# # Get the directory of the script
# script_dir = os.path.dirname(os.path.abspath(__file__))

# def calculate_player_form(input_path, output_path):
#     player_data = pd.read_csv(input_path)

#     # sort by Player_Name and Year
#     player_data.sort_values(by=["Player_Name", "Year"], inplace=True)

#     # calculate rolling average of runs scored (last 5 matches)
#     player_data["Runs_Form"] = player_data.groupby("Player_Name")["Runs_Scored"].transform(
#         lambda x: x.rolling(window=5, min_periods=1).mean()
#         )

#     # save updated data
#     player_data.to_csv(output_path, index=False)

# if __name__ == "__main__":
#     # define input and output paths
#     input_path = os.path.join(script_dir, "../../data/processed/cleaned_player_performance.csv")
#     output_path = os.path.join(script_dir, "../../data/processed/player_form.csv")

#     # runt the function
#     calculate_player_form(input_path, output_path)
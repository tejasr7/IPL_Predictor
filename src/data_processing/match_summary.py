import os
import json
import pandas as pd

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the folder containing JSON files
json_folder = os.path.join(script_dir, "../../data/raw/ipl_json/")

# Path to the output CSV file
output_csv_path = os.path.join(script_dir, "../../data/processed/match_summary.csv")

# Create the output directory if it doesn't exist
os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)

# List to store match summaries
match_summaries = []

# Loop through all JSON files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        # Load JSON file
        with open(os.path.join(json_folder, filename), "r") as file:
            match_data = json.load(file)

        # Extract match summary with error handling for missing keys
        try:
            match_summary = {
                "Match_ID": match_data["info"]["event"].get("match_number", "unknown"),
                "Teams": match_data["info"].get("teams", ["unknown", "unknown"]),
                "Venue": match_data["info"].get("venue", "unknown"),
                "Toss_Winner": match_data["info"].get("toss", {}).get("winner", "unknown"),
                "Toss_Decision": match_data["info"].get("toss", {}).get("decision", "unknown"),
                "Winner": match_data["info"].get("outcome", {}).get("winner", "unknown"),
                "Margin_Runs": match_data["info"].get("outcome", {}).get("by", {}).get("runs"),
                "Margin_Wickets": match_data["info"].get("outcome", {}).get("by", {}).get("wickets"),
                "Player_of_Match": match_data["info"].get("player_of_match", ["unknown"])[0]
            }
        except KeyError as e:
            print(f"Warning: Missing key {e} in file: {filename}")
            continue  # Skip this file and move to the next one

        # Append to the list
        match_summaries.append(match_summary)

# Convert to DataFrame
match_summary_data = pd.DataFrame(match_summaries)

# Save to CSV
match_summary_data.to_csv(output_csv_path, index=False)

print("Match summaries extracted and saved to CSV!")
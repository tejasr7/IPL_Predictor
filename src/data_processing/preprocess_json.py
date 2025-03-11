import os
import json
import pandas as pd

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the folder containing JSON files
json_folder = os.path.join(script_dir, "../../data/raw/ipl_json/")

# List to store ball-by-ball data
ball_by_ball_data = []

# Loop through all JSON files in the folder
for filename in os.listdir(json_folder):
    if filename.endswith(".json"):
        # Load JSON file
        with open(os.path.join(json_folder, filename), "r") as file:
            match_data = json.load(file)

        # Extract match metadata
        match_id = match_data["info"]["event"].get("match_number", "unknown")
        teams = match_data["info"]["teams"]
        venue = match_data["info"]["venue"]
        toss_winner = match_data["info"]["toss"]["winner"]
        toss_decision = match_data["info"]["toss"]["decision"]
        winner = match_data["info"]["outcome"].get("winner", "unknown")
        margin = match_data["info"]["outcome"]["by"].get("runs") if "by" in match_data["info"]["outcome"] else None
        player_of_match = match_data["info"].get("player_of_match", ["unknown"])[0]

        # Extract ball-by-ball data
        for inning in match_data["innings"]:
            team = inning["team"]
            for over in inning["overs"]:
                over_num = over["over"]
                for delivery in over["deliveries"]:
                    ball_by_ball_data.append({
                        "Match_ID": match_id,
                        "Teams": teams,
                        "Venue": venue,
                        "Toss_Winner": toss_winner,
                        "Toss_Decision": toss_decision,
                        "Winner": winner,
                        "Margin": margin,
                        "Player_of_Match": player_of_match,
                        "Inning": team,
                        "Over": over_num,
                        "Batter": delivery["batter"],
                        "Bowler": delivery["bowler"],
                        "Runs": delivery["runs"]["total"],
                        "Extras": delivery.get("extras", {}).get("total", 0),
                        "Wicket": 1 if "wickets" in delivery else 0
                    })

# Convert the list to a DataFrame
ball_by_ball_df = pd.DataFrame(ball_by_ball_data)

# Ensure the output directory exists
output_dir = os.path.join(script_dir, "../../data/processed/")
os.makedirs(output_dir, exist_ok=True)

# Save to CSV
output_path = os.path.join(output_dir, "ball_by_ball_data.csv")
ball_by_ball_df.to_csv(output_path, index=False)

print("Ball-by-ball data extracted and saved to CSV!")


# import os 
# import json
# import pandas as pd

# script_dir = os.path.dirname(os.path.abspath(__file__))
# json_folder = os.path.join(script_dir, "../../data/raw/ipl_json/")

# # path to the folder containing JSON files
# #json_folder = "../data/raw/ipl_json/"

# # list to store ball-by-ball data
# ball_by_ball_data = []

# # loop through all JSON files in the folder
# for filename in os.listdir(json_folder):
#     if filename.endswith(".json"):
#         # Load JSON file
#         with open(os.path.join(json_folder, filename),"r") as file:
#             match_data = json.load(file)

#         # Extract match metadata
#         match_id = match_data["info"]["event"]["match_number"]
#         teams = match_data["info"]["teams"]
#         venue = match_data["info"]["venue"]
#         toss_winner = match_data["info"]["toss"]["winner"]
#         toss_decision = match_data["info"]["toss"]["decision"]
#         winner = match_data["info"]["outcome"]["winner"]
#         margin = match_data["info"]["outcome"]["by"]["runs"] if "runs" in match_data["info"]["outcome"]["by"] else None
#         player_of_match = match_data["info"]["player_of_match"][0]


#         # Extract ball-by-ball data
#         for inning in match_data["innings"]:
#             team = inning["team"]
#             for over in inning["overs"]:
#                 over_num = over["over"]
#                 for delivery in over["deliveries"]:
#                     ball_by_ball_records.append({
#                         "Match_ID": match_id,
#                         "Teams": teams,
#                         "Venue": venue,
#                         "Toss_Winner": toss_winner,
#                         "Toss_Decision": toss_decision,
#                         "Winner": winner,
#                         "Margin": margin,
#                         "Player_of_Match": player_of_match,
#                         "Inning": team,
#                         "Over": over_num,
#                         "Batter": delivery["batter"],
#                         "Bowler": delivery["bowler"],
#                         "Runs": delivery["runs"]["total"],
#                         "Extras": delivery.get("extras", {}).get("total", 0),
#                         "Wicket": 1 if "wickets" in delivery else 0
#                     })


# # convert the DataFrame
# ball_by_ball_data = pd.DataFrame(ball_by_ball_data)

# # save to csv
# ball_by_ball_data.to_csv("../data/processed/ball_by_ball_data.csv", index=False)

# print("Ball-by-ball data extracted and saved to CSV!")



import pandas as pd

def initialize_elo_ratings(player_data):
    """
    Initialize Elo ratings for all players (default 1500)
    Args: 
        player_data (pd.DataFrame): DataFrame containing player data
    Returns:
        dict: Dictionary of player Elo ratings
    """

    return {player: 1500 for player in player_data["Player_Name"].unique()}

def update_elo(winner_elo, loser_elo, K=32):
    """
    Update Elo ratings after a match or performance comparison.

    Args:
        winner_elo (float): current elo rating of the winner.
        loser_elo (float): current elo rating of the loser.
        K (int): K-factor (default 32)

    returns: 
        tuple: updated Elo ratings for winner and loser.
    """
    expected_win = 1 / (1 + 10 ** ((loser_elo - winner_elo) / 400))
    winner_new = winner_elo + K * (1 - expected_win)
    loser_new = loser_elo + K * (0 - expected_win)
    return winner_new, loser_new

def calculate_elo_ratings(player_data, elo_dict):
    """
    calculate and update elo ratings for players based on their performance.

    Args:
        player_data (pd.DataFrame): DataFrame containing player performance data.
        elo_dict (dict): Dictionary of current Elo ratings.

    Returns:
        dict: updated elo ratings.
    """

    # Ensure "Runs_Scored" is numeric
    player_data["Runs_Scored"] = pd.to_numeric(player_data["Runs_Scored"], errors="coerce")
    player_data["Wickets_Taken"] = pd.to_numeric(player_data["Wickets_Taken"], errors="coerce")


    # Handle missing values (e.g., fill with 0)
    player_data["Runs_Scored"].fillna(0, inplace=True)
    player_data["Wickets_Taken"].fillna(0, inplace=True)


    for index, row in player_data.iterrows():
        player = row["Player_Name"]
        runs = row["Runs_Scored"]
        wickets = row["Wickets_Taken"]

        # Get current Elo
        player_elo = elo_dict[player]

        # Example logic for updating elo based on performnace
        if runs > 50: # reward for scoring more than 50 runs
            elo_dict[player] += 10
        elif runs < 10: # penalty for scoring less than 10 runs
            elo_dict[player] -= 5

        if wickets >= 2: # reward for taking 2 or more wickets
            elo_dict[player] += 10
        elif wickets == 0: # penalty for taking no wickets
            elo_dict[player] -= 5

    return elo_dict

def save_elo_ratings(elo_dict, output_path):
    """
    save elo ratings to csv.
    args:
        elo_dict (dict): dictionary of elo ratings.
    """
    elo_ratings = pd.DataFrame(elo_dict.items(), columns=["Player_Name", "Elo"])
    elo_ratings.to_csv(output_path, index=False)

if __name__ == "__main__":
    # load player data
    player_data = pd.read_csv("../../data/processed/cleaned_player_performance_new.csv")
    # player_data = pd.read_csv("../../data/processed/player_form.csv")

    # initializing elo ratings
    elo_dict = initialize_elo_ratings(player_data)

    # calculate and update elo ratings
    elo_dict = calculate_elo_ratings(player_data, elo_dict)

    # save elo ratings
    save_elo_ratings(elo_dict, "../../data/processed/player_elo_ratings.csv")


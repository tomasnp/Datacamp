"""
This script prepares the data for the analysis. 
It creates two dataframes: one containing all the matches and another containing all the events.
"""

import json
import os
import pandas as pd
from tqdm import tqdm

# Define the file paths
# PATH_STATBOMB = "data/statbomb/"
PATH_STATBOMB = "../open-data/data/"

# =============================================================================
# Create Matches dataframe


def get_matches(folders_path, path_save="data/", file_name="matches.csv"):
    """
    This function creates and saves a dataframe containing all the matches from the specified json files.

    Parameters
    ----------
    folders_path : str
        The path to the folder containing the matches.

    path_save : str
        The path to save the dataframe.

    file_name : str
        The name of the file to save the dataframe.
    """
    matches = pd.DataFrame()

    # Load and iterate over all the matches
    for subdir, dirs, files in tqdm(os.walk(folders_path)):
        for file in files:

            # Keep only the JSON files
            if file.endswith(".json"):
                filepath = subdir + os.sep + file

                with open(filepath, "r") as f:
                    data = json.load(f)
                    data = pd.json_normalize(data)

                matches = pd.concat([matches, data], ignore_index=True)

    # Compute relevant information
    matches["match_date"] = pd.to_datetime(matches["match_date"])
    matches["match_outcome"] = matches["home_score"] - matches["away_score"]
    matches["competition_season"] = matches["competition.competition_name"] + "_" + \
                                    matches["season.season_name"]

    # Save the matches to a CSV file
    matches.to_csv(path_save + file_name, index=False)

# =============================================================================
# Create Events dataframe


def get_events(matches, dir_path, path_save="data/", file_name="events.csv"):
    """
    This function creates and saves a dataframe containing all the events from the specified json files.

    Parameters
    ----------
    matches : pd.DataFrame
        The dataframe containing the matches.

    dir_path : str
        The path to the folder containing the events.

    path_save : str
        The path to save the dataframe.

    file_name : str
        The name of the file to save the dataframe.
    """
    events = pd.DataFrame()

    # Get the file names of the matches
    id_matchs = matches["match_id"].unique().astype(str)
    filename_matches = [x + ".json" for x in id_matchs]

    # Iterate over all the matches
    for roots, dirs, files in tqdm(os.walk(dir_path)):

        # Iterate over all the files in the directory
        for file in filename_matches:
            filepath = os.path.join(roots, file)

            # Load the data
            with open(filepath, "r") as f:
                data = json.load(f)
                data = pd.json_normalize(data)

            # Get relevant information from the matches
            match_id = file.split(".")[0]
            sub_matches = matches[matches["match_id"] == int(match_id)]

            # Add the relevant information to the dataframe
            data["match_id"] = match_id
            data["competition_season"] = sub_matches["competition_season"].iloc[0]
            data["match_date"] = sub_matches["match_date"].iloc[0]
            data["match_outcome"] = sub_matches["match_outcome"].iloc[0]
            data["home_team"] = sub_matches["home_team.home_team_name"].iloc[0]
            data["away_team"] = sub_matches["away_team.away_team_name"].iloc[0]
            data["away_score"] = sub_matches["away_score"].iloc[0]
            data["home_score"] = sub_matches["home_score"].iloc[0]

            # Move the columns to the front
            cols = data.columns.tolist()
            cols = cols[-8:] + cols[:-8]
            data = data[cols]

            events = pd.concat([events, data], ignore_index=True)

    events = events[events["period"] <= 4]
    events.to_csv(path_save + file_name, index=False)
    return events


# =============================================================================
# Main function
if __name__ == "__main__":
    print("Data preparation started...")
    matches = get_matches(PATH_STATBOMB)
    matches = pd.read_csv("data/matches.csv")
    get_events(matches, PATH_STATBOMB)
    print("Data preparation completed.")

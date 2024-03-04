import pandas as pd
import numpy as np
import matplotlib.patches as patches


class utils:
    def plot_field(self,ax):
        """
        Draw a football field on the given axes.

        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to draw the field.

        Returns:
        None
        """
        # terrain
        ax.plot([0,0],[0,80], color = "black")
        ax.plot([0,120],[80,80], color = "black")
        ax.plot([120,120],[80,0], color = "black")
        ax.plot([120,0],[0,0], color = "black")
        # surface de réparation
        ax.plot([0,18],[18,18], color = "black")
        ax.plot([0,18],[62,62], color = "black")
        ax.plot([120,102],[18,18], color = "black")
        ax.plot([120,102],[62,62], color = "black")
        ax.plot([18,18],[18,62], color = "black")
        ax.plot([102,102],[18,62], color = "black")
        # petit rectangle
        ax.plot([0,6],[30,30], color = "black")
        ax.plot([0,6],[50,50], color = "black")
        ax.plot([120,114],[30,30], color = "black")
        ax.plot([120,114],[50,50], color = "black")
        ax.plot([6,6],[30,50], color = "black")
        ax.plot([114,114],[30,50], color = "black")

        # point central
        ax.scatter(60,40, color = "black",s = 15)
        ax.plot([60,60],[80,0], color = "black")

        # point de penalty
        ax.scatter(12,40, color = "black",s = 15)
        ax.scatter(108,40, color = "black",s = 15)

        # Create the arc patch
        arc1 = patches.Arc((12, 40), 19, 19, angle=180, theta1=130, theta2=230, color='black')
        arc2 = patches.Arc((108, 40), 19, 19, angle=180, theta1=310, theta2=50, color='black')

        ax.add_patch(arc1)
        ax.add_patch(arc2)

        # rond central

        rond = patches.Arc((60, 40), 19, 19, angle=0, theta1=0, theta2=360, color='black')

        ax.add_patch(rond)


        # point de corner
        ax.scatter(0,0, color = "black")
        ax.scatter(120,0, color = "black")
        ax.scatter(0,80, color = "black")
        ax.scatter(120,80, color = "black")
    
    def assign_xg_to_team(self, row, xg_data):
        """
        Assigns the xG value to the team that scored the goal in the match event data frame.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        xg_data : pandas.DataFrame
            The expected goals data frame.

        Returns:
        -------
        pandas.Series
            A pandas series containing the xG value for the team that scored the goal.
        """
        home_xg = xg_data.loc[(xg_data['match_id'] == row['match_id']) & (
            xg_data['team.name'] == row['home_team']), 'xg_total'].sum()
        away_xg = xg_data.loc[(xg_data['match_id'] == row['match_id']) & (
            xg_data['team.name'] == row['away_team']), 'xg_total'].sum()
        return pd.Series([home_xg, away_xg])

    def calculate_total_form_xg(self, df, team_id_col):
        """
        Calculates the total form in xG for each team in the match event data frame.

        Parameters:
        ----------
        df : pandas.DataFrame
            The match event data frame.

        team_id_col : str
            The name of the column containing the team id.

        Returns:
        -------
        pandas.Series
            A pandas series containing the total form in xG for each team.
        """
        df_sorted = df.sort_values(by=['match_date', team_id_col])

        total_form_xg = []
        for index, row in df.iterrows():
            team_id = row[team_id_col]
            match_date = row['match_date']

            # Select the last 3 matches of the team, regardless of whether they play at home or away
            past_matches = df_sorted[((df_sorted['home_team'] == team_id) | (
                df_sorted['away_team'] == team_id)) & (df_sorted['match_date'] < match_date)].tail(3)

            # Accumulate xG regardless of home/away status
            team_xg_sum = 0
            for _, match in past_matches.iterrows():
                if match['home_team'] == team_id:
                    team_xg_sum += match['xg_total_home']

                elif match['away_team'] == team_id:
                    team_xg_sum += match['xg_total_away']

            total_form_xg.append(team_xg_sum)

        return pd.Series(total_form_xg)

    def calculate_adversary_form_xg(self, df, team_id_col):
        """
        Calculates the form in xG for the adversary team in the match event data frame.

        Parameters:
        ----------
        df : pandas.DataFrame
            The match event data frame.

        team_id_col : str
            The name of the column containing the team id.

        Returns:
        -------
        pandas.Series
            A pandas series containing the form in xG for the adversary team.
        """
        df_sorted = df.sort_values(by=['match_date', team_id_col])

        adversary_form_xg = []
        for index, row in df.iterrows():
            team_id = row[team_id_col]
            match_date = row['match_date']
            # Sélectionner les 3 derniers matchs de l'équipe, indépendamment du fait qu'elle joue à domicile ou à l'extérieur
            past_matches = df_sorted[((df_sorted['home_team'] == team_id) | (
                df_sorted['away_team'] == team_id)) & (df_sorted['match_date'] < match_date)].tail(3)

            adversary_xg_sum = 0
            for _, match in past_matches.iterrows():
                # Accumulate xG regardless of home/away status
                if match['home_team'] == team_id:
                    # Adversary xG at home
                    adversary_xg_sum += match['xg_total_away']

                elif match['away_team'] == team_id:
                    # Adversary xG away
                    adversary_xg_sum += match['xg_total_home']

            # Append the adversary form xG to the list
            adversary_form_xg.append(adversary_xg_sum)

        return pd.Series(adversary_form_xg)

    def calculate_form(self, df, team_id_col):

        # Sort the data frame by match date and team id
        df_sorted = df.sort_values(by=['match_date', team_id_col])

        # Iterate over the rows of the data frame
        form = []
        for index, row in df.iterrows():
            team_id = row[team_id_col]
            match_date = row['match_date']
            # Select the last 3 matches of the team, regardless of whether they play at home or away
            past_matches = df_sorted[((df_sorted['home_team'] == team_id) | (
                df_sorted['away_team'] == team_id)) & (df_sorted['match_date'] < match_date)].tail(3)

            team_form = 0
            for _, match in past_matches.iterrows():
                # Accumulate form regardless of home/away status
                if match['home_team'] == team_id:
                    if match['home_score'] > match['away_score']:
                        team_form += 1

                    elif match['home_score'] < match['away_score']:
                        team_form -= 1

                elif match['away_team'] == team_id:
                    if match['home_score'] < match['away_score']:
                        team_form += 1

                    elif match['home_score'] > match['away_score']:
                        team_form -= 1

            form.append(team_form)

        return pd.Series(form)

    def map_location_to_xT(self, x, y, xT_values):
        """
        Maps the x and y coordinates to the xT grid.

        Parameters:
        ----------
        x : int
            The x coordinate.

        y : int
            The y coordinate.

        xT_values : numpy.ndarray
            The xT grid.

        Returns:
        -------
        float
            The xT value at the given coordinates.
        """
        # Map the x and y coordinates to the xT grid
        xT_x = min(int(np.floor(float(x) / 120 * 16)), 15)
        xT_y = min(int(np.floor(float(y) / 80 * 12)), 11)
        return xT_values[xT_y, xT_x]

    def get_outcome(self, row):
        """
        Returns the outcome of the match event.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        Returns:
        -------
        str
            The outcome of the match event.
        """
        if row["type.name"] == "Pass":
            return row["pass.outcome.name"]

        elif row["type.name"] == "Dribble":
            return row["dribble.outcome.name"]

        elif row["type.name"] == "Shot":
            return row["shot.outcome.name"]

        else:
            return None

    def get_end_location(self, row, events):
        """
        Returns the end location of the match event.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        events : pandas.DataFrame
            The match event data frame.

        Returns:
        -------
        str
            The end location of the match event.
        """
        if pd.notnull(row['pass.end_location']):
            return row['pass.end_location']

        elif pd.notnull(row['shot.end_location']):
            return row['shot.end_location']

        elif pd.notnull(row['carry.end_location']):
            return row['carry.end_location']

        # If the event is a dribble, the end location is the start location of the next event
        elif row["type.name"] == "Dribble":
            row_index = row.name
            next_index = row_index + 1

            # Check if next_index exists
            if next_index in events.index:
                next_event = events.loc[next_index]
                return next_event.get("carry.end_location")
        else:
            return row['location']

    def remove_brackets(self, x):
        """
        Removes the brackets from the string.

        Parameters:
        ----------
        x : str
            The string.

        Returns:
        -------
        str
            The string without brackets.
        """
        if x[-1] == "]":
            return x[:-1]

        elif x[0] == "[":
            return x[1:]

        else:
            return x

    def get_end_x(self, row):
        """
        Returns the x coordinate of the end location of the match event.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        Returns:
        -------
        float
            The x coordinate of the end location of the match event.
        """
        if pd.notnull(row['end_location']):
            return float(self.remove_brackets(row['end_location'].split(",")[0]))

        else:
            return None

    def get_end_y(self, row):
        """
        Returns the y coordinate of the end location of the match event.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        Returns:
        -------
        float
            The y coordinate of the end location of the match event.
        """

        if pd.notnull(row['end_location']):
            return float(self.remove_brackets(row['end_location'].split(",")[1]))

        else:
            return None

    def get_end_z(self, row):
        """
        Returns the z coordinate of the end location of the match event.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        Returns:
        -------
        float
            The z coordinate of the end location of the match event.
        """
        if pd.notnull(row['end_location']) and row['type.name'] == 'Shot':
            return float(self.remove_brackets(row['end_location'].split(",")[-1]))

        else:
            return 0

    def get_end_xT(self, row, xT_values):
        """
        Returns the xT value of the end location of the match event.

        Parameters:
        ----------
        row : pandas.Series
            The row of the match event data frame.

        xT_values : numpy.ndarray
            The xT grid.

        Returns:
        -------
        float
            The xT value of the end location of the match event.
        """
        if pd.notnull(row['end_x']):
            return self.map_location_to_xT(row['end_x'], row['end_y'], xT_values)

        else:
            return None
        
    def extract_player_names(self, tactics_lineup):
        """
        Extract the names of the players from the tactics lineup
        
        Parameters:
        ----------
        tactics_lineup: list of dictionaries
            The list of players in the lineup

        Returns:
        -------
        list
            The list of players' names
        """
        return [player["player"]["name"] for player in tactics_lineup]

    def extract_player_position(self, tactics_lineup):
        """
        Extract the position of the players from the tactics lineup

        Parameters:
        ----------
        tactics_lineup: list of dictionaries
            The list of players in the lineup

        Returns:
        -------
        list
            The list of players' positions
        """
        return [player["position"]["name"] for player in tactics_lineup]

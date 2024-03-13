import os
import sys

# Assuming your current script is within 'shot_1_analysis' directory,
# we navigate two levels up to reach the Django project root ('swing_visionV1')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)

# Now attempting the import; adjust if your actual import path differs
from data_analysis.sheets_credentials.data_frames import workbook_to_df, get_shots_df, get_points_df

import pandas as pd

shots_df = get_shots_df()
points_df = get_points_df()

# Merging the dataframes on 'Point', 'Game', and 'Set' columns
merged_df = pd.merge(shots_df, points_df, left_on=['Point', 'Game', 'Set'], right_on=['Point Number', 'Game', 'Set'], how='left')

#Totals number of points won based off serve spin (Ex: Flat, spin, slice)
def calculate_serve_win_percentage(merged_df):
    # Initialize counters for each serve type
    serve_counts = {}
    wins_counts = {}

    # Iterate through the DataFrame
    for _, serve in merged_df.iterrows():
        # Check if the shot is a serve
        if serve['Type'].lower().startswith('serve'):
            # Extract the player name and spin type
            player = serve['Player'].split('_')[0]  # Assumes "Player1first_serve" format
            spin = serve['Spin']

            # Initialize counters for this spin type if not already done
            if spin not in serve_counts:
                serve_counts[spin] = 0
                wins_counts[spin] = 0

            # Increment the total count for the serve type
            serve_counts[spin] += 1

            # Check if the point was won by the server
            if serve['Point Winner'] == 'host':
                wins_counts[spin] += 1

    # Calculate win percentages for each serve type
    win_percentages = {}
    for spin, count in serve_counts.items():
        if count > 0:
            win_percentage = (wins_counts[spin] / count) * 100
            win_percentages[spin] = win_percentage
        else:
            win_percentages[spin] = 0  # If no serves of this type, set win percentage to 0

    return win_percentages

# Example usage
win_percentages = calculate_serve_win_percentage(merged_df)
for spin, win_percentage in win_percentages.items():
    print(f"{spin} Serve: {win_percentage:.2f}% points won")


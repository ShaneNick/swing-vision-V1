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
def calculate_player_serve_win_percentage_losses_and_ratios(merged_df):
    serve_counts = {}  # Tracks total serves by type
    wins_counts = {}  # Tracks wins by serve type
    losses_counts = {}  # Tracks losses by serve type

    for _, row in merged_df.iterrows():
        player_as_str = str(row['Player'])
        serve_type = str(row['Type']).lower()

        if player_as_str.startswith('Player') and (serve_type.startswith('first_serve') or serve_type.startswith('second_serve')):
            spin = row['Spin']
            point_winner = row['Point Winner']
            
            if spin not in serve_counts:
                serve_counts[spin] = 0
                wins_counts[spin] = 0
                losses_counts[spin] = 0
            
            serve_counts[spin] += 1
            if point_winner == 'host':
                wins_counts[spin] += 1
            elif point_winner == 'guest':
                losses_counts[spin] += 1

    output_data = {}
    for spin, total_serves in serve_counts.items():
        wins = wins_counts[spin]
        losses = losses_counts[spin]
        win_percentage = (wins / total_serves) * 100
        win_ratio = f"{wins}/{total_serves}"
        loss_ratio = f"{losses}/{total_serves}"
        output_data[spin] = {"Win Percentage": win_percentage, "Wins Ratio": win_ratio, "Losses": losses, "Loss Ratio": loss_ratio}

    return output_data

player_stats = calculate_player_serve_win_percentage_losses_and_ratios(merged_df)
for spin, stats in player_stats.items():
    print(f"{spin} Serve: {stats['Win Percentage']:.2f}% points won, Wins ({stats['Wins Ratio']}),  {stats['Losses']} losses ({stats['Loss Ratio']})")


print("---------")

def analyze_serve_speed_spin_success(merged_df):
    # Define comprehensive speed bins
    speed_bins = [(0, 50), (50, 60), (60, 70), (70, 80), (80, 90), (90, 100), (100, float('inf'))]
    speed_labels = ['<50 MPH', '50-60 MPH', '60-70 MPH', '70-80 MPH', '80-90 MPH', '90-100 MPH', '100+ MPH']
    
    # Initialize results dictionary to store data
    results = {}
    
    for _, row in merged_df.iterrows():
        # Additional filtering conditions
        if row['Player'] != 'Player' or (row['Type'] != 'first_serve' and row['Type'] != 'second_serve'):
            continue  # Skip the row if it doesn't meet the criteria
        
        serve_speed = row['Speed (MPH)']
        serve_spin = row['Spin']
        point_winner = row['Point Winner']

        # Identify the correct speed bin for each serve
        for (min_speed, max_speed), label in zip(speed_bins, speed_labels):
            if min_speed <= serve_speed < max_speed:
                speed_label = label
                break

        # Construct a unique key for each speed and spin type combination
        key = f"{speed_label} {serve_spin}"
        
        # Initialize or update the counts for each combination
        if key not in results:
            results[key] = {'total_serves': 0, 'wins': 0, 'losses': 0}
        results[key]['total_serves'] += 1
        if point_winner == 'host':
            results[key]['wins'] += 1
        else:
            results[key]['losses'] += 1

    # Print the results for each combination of speed and spin
    for key, data in results.items():
        win_percentage = (data['wins'] / data['total_serves']) * 100 if data['total_serves'] > 0 else 0
        print(f"{key}: {win_percentage:.2f}% wins ({data['wins']}/{data['total_serves']} wins), {data['losses']} losses")

# Ensure merged_df is defined as per your earlier setup before calling this function
analyze_serve_speed_spin_success(merged_df)












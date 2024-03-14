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

def calculate_serve_win_percentage_losses_and_direction_ratios(merged_df):
    serve_counts = {}
    wins_counts = {}
    losses_counts = {}
    direction_counts = {}

    total_serves = 0

    for _, row in merged_df.iterrows():
        if "Player" in str(row['Player']) and row['Type'] in ['first_serve', 'second_serve']:
            spin = row['Spin']
            direction = row['Direction']
            point_winner = row['Point Winner']

            if spin not in serve_counts:
                serve_counts[spin] = 0
                wins_counts[spin] = 0
                losses_counts[spin] = 0
                direction_counts[spin] = {}

            if direction not in direction_counts[spin]:
                direction_counts[spin][direction] = {'total': 0, 'wins': 0, 'losses': 0}

            serve_counts[spin] += 1
            total_serves += 1
            direction_counts[spin][direction]['total'] += 1

            if point_winner == 'host':
                wins_counts[spin] += 1
                direction_counts[spin][direction]['wins'] += 1
            elif point_winner == 'guest':
                losses_counts[spin] += 1
                direction_counts[spin][direction]['losses'] += 1

    output_data = {}
    for spin, dir_stats in direction_counts.items():
        spin_total = serve_counts[spin]
        spin_wins = wins_counts[spin]
        spin_losses = losses_counts[spin]
        spin_win_percentage = (spin_wins / spin_total) * 100 if spin_total > 0 else 0
        output_data[spin] = {"Win Percentage": f"{spin_win_percentage:.2f}%", "Total Serves": spin_total, "Wins": spin_wins, "Losses": spin_losses, "Directions": {}}
        for direction, counts in dir_stats.items():
            dir_win_percentage = (counts['wins'] / counts['total']) * 100 if counts['total'] > 0 else 0
            output_data[spin]["Directions"][direction] = {
                "Win Percentage": f"{dir_win_percentage:.2f}%",
                "Wins/Losses": f"{counts['wins']}/{counts['losses']}",
                "Total Serves": counts['total'],
                "Percentage of Spin Total": f"{(counts['total'] / spin_total) * 100:.2f}%",
                "Percentage of All Serves": f"{(counts['total'] / total_serves) * 100:.2f}%"
            }

    return output_data

# Example usage
# Example usage and output formatting
player_stats = calculate_serve_win_percentage_losses_and_direction_ratios(merged_df)
for spin, stats in player_stats.items():
    print(f"Spin Type: {spin}")
    print(f"  Overall Win Percentage for {spin} Serves: {stats['Win Percentage']} (Calculated as Wins/Total Serves)")
    print(f"  Total {spin} Serves: {stats['Total Serves']}")
    print(f"  Wins with {spin} Serves: {stats['Wins']}")
    print(f"  Losses with {spin} Serves: {stats['Losses']}")
    
    for direction, dir_stats in stats["Directions"].items():
        print(f"    Direction: {direction}")
        print(f"    Win Percentage in this Direction: {dir_stats['Win Percentage']} (Wins/Losses for {direction})")
        print(f"    Total Serves in this Direction: {dir_stats['Total Serves']}")
        print(f"    This Direction as a Percentage of Total {spin} Serves: {dir_stats['Percentage of Spin Total']}%")
        print(f"    This Direction as a Percentage of All Serves: {dir_stats['Percentage of All Serves']}%")

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

print("---------")












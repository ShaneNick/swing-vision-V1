from ..sheets_credentials.data_frames import workbook_to_df, get_shots_df, get_points_df
import pandas as pd

shots_df = get_shots_df()
points_df = get_points_df()

# Merging the dataframes on 'Point', 'Game', and 'Set' columns
merged_df = pd.merge(shots_df, points_df, left_on=['Point', 'Game', 'Set'], right_on=['Point Number', 'Game', 'Set'], how='left')

# Print the first 10 rows of the merged dataframe for inspection
print(merged_df.head(10))

from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from .sheets_cred import connection_to_google_API

def workbook_to_df(worksheet):
    try:
        records = worksheet.get_all_records()
        return pd.DataFrame.from_records(records)
    except Exception as e:
        print(f"Error converting sheet to Dataframe: {e}")
        raise

def get_shots_df():
    workbook_key = '1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU'
    client = connection_to_google_API()
    shots_sheet = client.open_by_key(workbook_key).worksheet('Shots')
    return workbook_to_df(shots_sheet)


def get_points_df():
    workbook_key = '1RDJh21agwb5YtVjBU-6IbAhHwNhpbeI5ATA-wYR4BiU'
    client = connection_to_google_API()
    points_sheet = client.open_by_key(workbook_key).worksheet('Points')
    return workbook_to_df(points_sheet)


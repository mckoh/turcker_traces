"""
TRUCKER TRACES LOADING AND PREPROCESSING FUNCTIONS
Author: Michael Kohelgger
Date: November 2025
"""


import pandas as pd
from datetime import datetime as dt, timedelta

def load_data(filepath, headers):
    data = pd.read_excel(filepath, header=None)
    data.columns = headers
    return data

def clean_data(data):
    data = data.loc[data.slot != "Steckplatz"]
    data = data.loc[data["truck_status"] != "Leer"]
    return data

def create_date_column(data, log_statuses):
    data.truck_status = data.truck_status.fillna("Leer")
    data["date"] = data.truck_status.map(lambda x: x if x not in log_statuses else None)
    data["date"] = data["date"].ffill()
    return data

def fix_time_columns(data):
    data["start_time"] = data["start_time"].map(lambda x: x.replace("24:", "00:"))
    data["end_time"] = data["end_time"].map(lambda x: x.replace("24:", "00:"))
    data["start"] = data["date"] + " " + data["start_time"]
    data["end"] = data["date"] + " " + data["end_time"]
    data["date"] = data["date"].map(lambda x: dt.strptime(x, "%d.%m.%Y"))
    return data

def filter_log_data(data, log_statuses):
    data["log_marker"] = data.truck_status.map(lambda x: x in log_statuses)
    data = data.loc[data.log_marker == True]
    data = data.loc[data["truck_status"] != "Leer"]
    return data

def parse_datetime(data):
    data["start"] = data["start"].map(lambda x: dt.strptime(x, "%d.%m.%Y %H:%M"))
    data["end"] = data["end"].map(lambda x: dt.strptime(x, "%d.%m.%Y %H:%M"))
    data.drop(["start_time", "end_time"], axis=1, inplace=True)
    return data

def calculate_duration(data):
    data["duration"] = (data["end"] - data["start"]).map(lambda x: x.total_seconds() / 60)
    data["duration"] = data["duration"].fillna(0)

    # Fix negative durations (overnight trips)
    mask = data["duration"] < 0
    data.loc[mask, "end"] = data.loc[mask, "end"] + timedelta(days=1)
    data["duration"] = (data["end"] - data["start"]).map(lambda x: x.total_seconds() / 60)
    data["duration"] = data["duration"].fillna(0)
    return data

def calculate_times(data):
    data["calculation_row"] = data["truck_status"].map(lambda x: x == "Solo")

    data.loc[data["task_code"] == "l", "driving_time"] = data["duration"]
    data["driving_time"] = data["driving_time"].fillna(0)

    data.loc[data["task_code"] == "a", "working_time"] = data["duration"]
    data["working_time"] = data["working_time"].fillna(0)

    data.loc[data["task_code"] == "r", "resting_time"] = data["duration"]
    data["resting_time"] = data["resting_time"].fillna(0)
    return data

def aggregate_times(data):
    calc_rows = data.loc[data["calculation_row"]]
    data["total_time"] = calc_rows.groupby("date")["duration"].transform("sum")
    data["total_driving_time"] = calc_rows.groupby("date")["driving_time"].transform("sum")
    data["total_working_time"] = calc_rows.groupby("date")["working_time"].transform("sum")
    data["total_resting_time"] = calc_rows.groupby("date")["resting_time"].transform("sum")
    return data

def process_data(filepath, headers, log_statuses):
    data = load_data(filepath, headers)
    data = clean_data(data)
    data = create_date_column(data, log_statuses)
    data = fix_time_columns(data)
    data = filter_log_data(data, log_statuses)
    data = parse_datetime(data)
    data = calculate_duration(data)
    data = calculate_times(data)
    data = aggregate_times(data)
    return data

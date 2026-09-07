import h5pyd # ?
import os
import pandas as pd
import pathlib
from rex import ResourceX

data_dir = "/nrel/nsrdb/GOES/aggregated/v4.0.0/"

years = [2024]
states = ["New York", "Maine", "New Hampshire", "Rhode Island", "Vermont", "Connecticut"]

attributes = ["air_temperature", "clearsky_ghi", "ghi", "relative_humidity", "surface_pressure", "wind_speed"]

for y in years:
    for attr in attributes:
        for s in states:

            save_folder = f"/home/emco4286/data/NSRDB_BY_STATE/{s}/"

            if not os.path.isdir(save_folder):
                os.mkdir(save_folder)

            save_name = f"nsrdb_{attr}_{y}.csv"
            save_pt = os.path.join(save_folder, save_name)

            if os.path.isdir(save_pt): # This does not work
                print(f"{save_name} already exists, skipping...")
                continue
            else:
                print(f"Pulling {attr} data from {y}")
                handler = ResourceX(os.path.join(data_dir, f"nsrdb_{y}.h5"))
                df = handler.get_region_df(attr, s)
                df.to_csv(save_pt)
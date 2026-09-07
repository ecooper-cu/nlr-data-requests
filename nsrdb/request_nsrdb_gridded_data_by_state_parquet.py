import h5pyd
import os
import pandas as pd
from rex import ResourceX
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", type=int)
args = parser.parse_args()

data_dir = "/nrel/nsrdb/GOES/aggregated/v4.0.0/"
hsds_kwargs = {'endpoint': 'https://developer.nlr.gov/api/hsds',
               'api_key' : '6ghV5seyAi2il2pQd9NVpavUEN9A6Zlm8IH0O2vl'}

states = ["Massachusetts", "New York", "Maine", "New Hampshire", "Rhode Island", "Vermont", "Connecticut"]

attributes = ["air_temperature", "clearsky_ghi", "ghi", "relative_humidity", "surface_pressure", "wind_speed"]

for attr in attributes:
    for s in states:

        save_folder = f"/home/emco4286/data/NSRDB_BY_STATE/{s}/{args.year}/"

        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)

        save_name = f"nsrdb_{attr}_{args.year}.parquet"
        save_pt = os.path.join(save_folder, save_name)

        alternative_save_name = f"nsrdb_{attr}_{args.year}.csv"
        alternative_save_pt = os.path.join(save_folder, alternative_save_name)

        if os.path.isfile(save_pt) or os.path.isfile(alternative_save_pt):
            print(f"{save_name} already exists for {s}, skipping...")
            continue
        else:
            print(f"Pulling {args.year} {attr} data from {s}")
            handler = ResourceX(os.path.join(data_dir, f"nsrdb_{args.year}.h5"))
            df = handler.get_region_df(attr, s)
            df.to_parquet(save_pt, engine='pyarrow')
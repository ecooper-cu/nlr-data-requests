
import h5pyd # ?
import os
import pandas as pd
import pathlib
from rex import ResourceX

years = [2042]
states = ["Maine", "New Hampshire", "Rhode Island", "Vermont", "Connecticut", "Massachusetts"]
attributes = ["temperature_2m", "ghi", "relativehumidity_2m", "pressure_0m", "windspeed_10m"]
data_dir = "/nrel/sup3rcc/conus_ecearth3cc_ssp245_r1i1p1f1/v0.2.2/"
files = [f'sup3rcc_conus_ecearth3cc_ssp245_r1i1p1f1_{y}.h5' for y in years]

for f, y in zip(files, years):

    print(f"Pulling data from {y}")
    handler = ResourceX(os.path.join(data_dir, f))
    meta = handler.meta
    ti = handler.time_index

    for s in states:
        print(f"Pulling data for {s}")

        mapping_pt = f"/home/emco4286/data/NSRDB_BY_STATE/Mappings/{s}.csv"
        save_folder = f"/home/emco4286/data/SUP3RCC_BY_STATE/{s}/"

        if not os.path.isdir(save_folder):
            os.mkdir(save_folder)

        for attribute in attributes:
            save_name = f"sup3rcc_{s}_{attribute}_{y}.parquet"
            save_pt = os.path.join(save_folder, save_name)
            if os.path.isfile(save_pt): # This does not work
                print(f"{save_name} already exists, skipping...")
                continue
            else:
                print(f"Pulling {attribute} data from {y} for {s}")
                df = handler.get_region_df(attribute, s)
                df.to_parquet(save_pt)

import os
import pandas as pd
import numpy as np
from rex import NSRDBX

network_pv = pd.read_excel("/home/emco4286/data/network.xlsx", sheet_name="PV")
network_eno = pd.read_excel("/home/emco4286/data/network.xlsx", sheet_name="ENO")

network_pv.set_index(network_pv["Name"], inplace=True)
network_eno.set_index(network_eno["Name"], inplace=True)

plant_to_coords = {}

for plant in network_pv.index:
    node = network_pv.loc[network_pv.index == plant, "NodeName"].values[0]
    lon = np.round(network_eno.loc[network_eno.index == node, "X/Long [-] = 0"].values[0], 2)
    lat = np.round(network_eno.loc[network_eno.index == node, "Y/Lat [-] = 0"].values[0], 2)
    plant_to_coords[plant] = (lat, lon)

data_dir = "/nrel/nsrdb/GOES/aggregated/v4.0.0/"
years = [2024, 2025]
attributes = ['air_temperature', 'dhi','dni','ghi']

plant_to_year_to_data = {p:{year: {} for year in years} for p in plant_to_coords.keys()}

for year in years:
    print(f"Pulling data for {year}...")
    nsrdb_file = os.path.join(data_dir, f"nsrdb_{year}.h5")
    with NSRDBX(nsrdb_file, hsds=True) as f:
        time_index = f.time_index
        for plant, location in plant_to_coords.items():
            for attr in attributes:
                print(f"Pulling {attr} data for {plant}...")
                data = f.get_lat_lon_df(attr, location)
                data.set_index(time_index, inplace=True)
                print(data.head())
                plant_to_year_to_data[plant][year][attr] = data

plant_to_data = {}
for plant in plant_to_coords.keys():
    data_list = []
    for year in years:
        data = pd.concat(plant_to_year_to_data[plant][year].values(), axis=1)
        data.columns = attributes
        data.set_index(plant_to_year_to_data[plant][year][attributes[0]].index, inplace=True)
        print(data.head())
        data_list.append(data)
    data = pd.concat(data_list, axis=0)
    data.columns = attributes
    data.to_csv(f"/home/emco4286/data/pv_nsrdb/2024/{plant}.csv")

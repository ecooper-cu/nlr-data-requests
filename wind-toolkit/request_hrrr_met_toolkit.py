import pandas as pd
import numpy as np
import os
from rex import WindX

network_wind = pd.read_excel("/home/emco4286/data/network.xlsx", sheet_name="WIND")
network_eno = pd.read_excel("/home/emco4286/data/network.xlsx", sheet_name="ENO")

network_wind.set_index(network_wind["Name"], inplace=True)
network_eno.set_index(network_eno["Name"], inplace=True)

plant_to_coords = {}

for plant in network_wind.index:
    node = network_wind.loc[network_wind.index == plant, "NodeName"].values[0]
    lon = np.round(network_eno.loc[network_eno.index == node, "X/Long [-] = 0"].values[0], 2)
    lat = np.round(network_eno.loc[network_eno.index == node, "Y/Lat [-] = 0"].values[0], 2)
    plant_to_coords[plant] = (lat, lon)

years = [2015, 2024, 2025]
attributes = ['windspeed_100m', 'pressure_100m', 'temperature_100m']

data_directory = '/nrel/wtk/hrrr_met_toolkit/v1.0.0/'

plant_to_year_to_data = {p:{year: {} for year in years} for p in plant_to_coords.keys()}

for year in years:
    print(f"Pulling data for {year}...")
    wtk_file = os.path.join(data_directory, f"hrrr_nat_f02_conus_{year}.h5")
    with WindX(wtk_file, hsds=True) as f:
        time_index = f.time_index
        for plant, location in plant_to_coords.items():
            print(f"Pulling data for {plant}")
            for attr in attributes:
                data = f.get_lat_lon_df(attr, location)
                data.set_index(time_index, inplace=True)
                plant_to_year_to_data[plant][year][attr] = data

plant_to_data = {}
for plant in plant_to_coords.keys():
    data_list = []
    for year in years:
        data = pd.concat(plant_to_year_to_data[plant][year].values(), axis=1)
        data.columns = attributes
        data.set_index(plant_to_year_to_data[plant][year][attributes[0]].index, inplace=True)
        print(f"Saving data for {plant}...")
        print(data.head())
        data.to_csv(f"/home/emco4286/data/wind/raw/{year}/{plant}.csv")
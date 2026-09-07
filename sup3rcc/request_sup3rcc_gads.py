
import h5pyd # ?
import os
import pandas as pd
import pathlib
from rex import ResourceX

data_dir = '/nrel/sup3rcc/conus_ecearth3cc_ssp245_r1i1p1f1/v0.2.2/'
# years = range(2041, 2053)
years = [2042, 2043]
files = [f'sup3rcc_conus_ecearth3cc_ssp245_r1i1p1f1_{y}.h5' for y in years]

coordinate_list = [
                   (41.94, -70.58),
                   (41.37, "-72.10"),
                   (42.90, -70.86),
                   (38.43, -76.44),
                   (39.47, -75.54),
                   (39.46, -75.53),
                   (39.76, -76.27),
                   (40.23, -75.58),
                   (41.09, -76.15),
                   (40.15, -76.71),
                   (40.62, -80.42),
                   (41.27, -73.95),
                   (43.52, -76.41),
                   (43.27, -77.31),
                   (35.23, -85.09),
                   (35.60, -84.79),
                   (35.63, -78.96),
                   (35.43, -80.94),
                   (38.06, -77.79),
                   (37.16, "-76.70")
                   ]

save_dir = os.path.join(pathlib.Path.home(), "data", "SUP3RCC_FOR_GADS")

hsds_kwargs = {'endpoint': 'https://developer.nlr.gov/api/hsds',
               'api_key' : '6ghV5seyAi2il2pQd9NVpavUEN9A6Zlm8IH0O2vl'}

for f, y in zip(files, years):

    print(f"Pulling data from {y}")

    handler = ResourceX(os.path.join(data_dir, f))
    meta = handler.meta
    ti = handler.time_index

    for coord in coordinate_list:
        gid = handler.lat_lon_gid((float(coord[0]), float(coord[1])))

        save_name = f"coord_{coord[0]}_{coord[1]}_year_{y}.csv"
        
        data = pd.DataFrame({"temp" : handler['temperature_2m', :, gid],
                              "ws10" : handler['windspeed_10m', :, gid],
                              "wd10" : handler['winddirection_10m', :, gid],
                              "ws100" : handler['windspeed_100m', :, gid],
                              "wd100" : handler['winddirection_100m', :, gid],
                              "ws200" : handler['windspeed_200m', :, gid],
                              "wd200" : handler['winddirection_200m', :, gid],
                              "ghi" : handler["ghi", :, gid],
                              "dhi": handler["dhi", :, gid],
                              "dni": handler["dni", :, gid],
                              "rh" : handler['relativehumidity_2m', :, gid],
                              "pressure_0m" : handler['pressure_0m', :, gid]}, index=ti)
        
        data.to_csv(os.path.join(save_dir, save_name))





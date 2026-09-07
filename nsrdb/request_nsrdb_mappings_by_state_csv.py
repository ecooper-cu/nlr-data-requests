import h5pyd
import pandas as pd
import json

with open("/home/emco4286/data/hsds_config.json",'r') as file:
	config_dict = json.load(file)
	
states = ["New York", "Maine", "New Hampshire", "Rhode Island", "Vermont", "Connecticut"]

f = h5pyd.File("/nrel/nsrdb/GOES/aggregated/v4.0.0/nsrdb_2012.h5")
meta = pd.DataFrame(f['meta'][...])

for s in states:
    data =  meta.loc[meta['state'] == s.encode()]
    data.to_csv(f"/home/emco4286/data/NSRDB_BY_STATE/Mappings/{s}.csv")
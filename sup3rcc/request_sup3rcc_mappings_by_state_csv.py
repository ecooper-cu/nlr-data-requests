import h5pyd
import pandas as pd
import json

with open("/home/emco4286/data/hsds_config.json",'r') as file:
	config_dict = json.load(file)
	
states = ["Maine", "New Hampshire", "Rhode Island", "Vermont", "Connecticut", "Massachusetts"]

y = 2042

f = h5pyd.File(f"/nrel/sup3rcc/conus_ecearth3cc_ssp245_r1i1p1f1/v0.2.2/sup3rcc_conus_ecearth3cc_ssp245_r1i1p1f1_{y}.h5")
meta = pd.DataFrame(f['meta'][...])

for s in states:
    data =  meta.loc[meta['state'] == s.encode()]
    data.to_csv(f"/home/emco4286/data/SUP3RCC_BY_STATE/Mappings/{s}.csv")
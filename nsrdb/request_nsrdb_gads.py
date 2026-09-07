import requests

coordinate_list = [
                   (41.94, -70.58),
                   (41.37, -72.10),
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
                   (37.16, -76.70),
                   (35.23, -85.09),
                   (35.60, -84.79),
                   (35.63, -78.96),
                   (35.43, -80.94),
                   (38.06, -77.79),
                   (37.16, -76.70)
                   ]

generator_names = ["Pilgrim 1",
                    "Millstone 2 & 3",
                    "Seabrook 1",
                    "Calvert Cliffs 1 & 2",
                    "Hope Creek 1",
                    "Oyster Creek",
                    "Peach Bottom 2 & 3",
                    "Limerick 1 & 2",
                    "Susquehanna 1 & 2",
                    "Three Mile Island 1",
                    "Beaver Valley 1 & 2",
                    "Indian Point 2 & 3",
                    "Nine Mile Point 1 & 2",
                    "Ginna",
                    "Davis-Besse",
                    "Sequoyah 1 & 2",
                    "Watts Bar 1 & 2",
                    "Harris 1",
                    "McGuire 1 & 2",
                    "North Anna 1 & 2",
                    "Surry 1 & 2"]

api_key = '6ghV5seyAi2il2pQd9NVpavUEN9A6Zlm8IH0O2vl'
email = "emco4286@colorado.edu"

url = f"https://developer.nlr.gov/api/nsrdb/v2/solar/nsrdb-GOES-aggregated-v4-0-0-download.json?api_key={api_key}"

years = ",".join(map(str, list(range(2013, 2025))))
attributes = 'air_temperature,clearsky_dhi,clearsky_dni,clearsky_ghi,dhi,dew_point,dni,ghi,relative_humidity,solar_zenith_angle,surface_albedo,surface_pressure,total_precipitable_water,wind_direction,wind_speed'
locations = "%2C".join(map(str, [f"{v[1]}%20{v[0]}" for v in coordinate_list]))

payload = f"api_key={api_key}&attributes={attributes}&names={years}&utc=false&leap_day=true&interval=30&email={email}&wkt=MULTIPOINT({locations})"

headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
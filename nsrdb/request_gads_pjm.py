import requests

coordinate_list = [
                  #  (42.08, -89.28),
                #    (42.08, -89.29),
                  #  (41.73, -90.3),
                #    (41.73, -90.4),
                  #  (41.24, -88.66),
                #    (41.24, -88.67),
                  #  (41.24, -88.22),
                #    (41.24, -88.23)
                   (34.72, -87.10),
                #    (41.38, 82.29)
                  #  (40.16, -88.80),
                  #  (41.60, -83.10),
                  #  (41.80, -81.14)
                   ]


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
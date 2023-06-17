import json
import requests
import time
import pickle
from datetime import date
#pirates cove marina doesnt apppear on the list
'''
with open (r"test2.json", "r") as file:
    data = json.load(file)

'''
bc_parks_ID_response = requests.get('https://camping.bcparks.ca/api/resourceLocation').text
bc_parks_ID_data = json.loads(bc_parks_ID_response)
count = 0
output_data = {}

with open ("bad-spots-r1.pickle", "rb") as file:
    bad_spots = pickle.load(file)
#obj = json.loads(data), 

for location in bc_parks_ID_data:
    resource_ID = location['resourceLocationId']
    name = location['localizedValues'][0]['fullName']
    if "Backcountry" in name:
        continue

    if name in bad_spots.keys():
        coordinates = bad_spots[name]
    else:
    
        name_w_plus = name.replace(" ", "+")
        osm_response = requests.get(f'https://nominatim.openstreetmap.org/?addressdetails=1&q={name_w_plus}&format=json&limit=1&state=British+Columbia').text
        time.sleep(2)
        osm_data = json.loads(osm_response)
        if osm_data == []:
            name = location['localizedValues'][0]['shortName']
            if name in bad_spots.keys():
                coordinates = bad_spots[name]
                print(output_tuple := (name, coordinates))
                output_data[resource_ID] = output_tuple
                continue
            else:
                name_w_plus = name.replace(" ", "+")
                osm_response = requests.get(f'https://nominatim.openstreetmap.org/?addressdetails=1&q={name_w_plus}&format=json&limit=1&state=British+Columbia').text
                time.sleep(2)
                osm_data = json.loads(osm_response)
                if osm_data == []:
                    print("failure")
                    exit()
        lat = float(osm_data[0]['lat'])
        lon = float(osm_data[0]['lon'])
        coordinates = [lon, lat]
    print(output_tuple := (name, coordinates))
    output_data[resource_ID] = output_tuple
    
    


with open(f'locationData-{date.today()}-2.pickle', 'wb') as f:
    pickle.dump(output_data, f, pickle.HIGHEST_PROTOCOL)
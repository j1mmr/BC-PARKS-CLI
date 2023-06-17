import json
import requests
import time
import pickle
from datetime import date
#pirates cove marina doesnt apppear on the list

with open (r"auth.json", "r") as file:
    data = json.load(file)

with open (r"bad-spots-r1.pickle", "rb") as file:
    bad_spots = pickle.load(file)

bc_parks_ID_response = requests.get('https://camping.bcparks.ca/api/resourceLocation').text
bc_parks_ID_data = json.loads(bc_parks_ID_response)
count = 0
output_data = {}
starting_point = [-123.1450236, 49.2450569]
ors_auth = data["ors_auth"]
ors_headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248f82140ae37c1474981d918825f667a52',
    'Content-Type': 'application/json; charset=utf-8'
}

#obj = json.loads(data), 
print(bad_spots)
for location in bc_parks_ID_data:
    resource_ID = location['resourceLocationId']
    name = location['localizedValues'][0]['fullName']
    if "Backcountry" in name: # this might have been a mistake...
        continue
    if name in bad_spots.keys():
        ending_point = bad_spots[name]
        print(name)
    else:
        
        name_w_plus = name.replace(" ", "+")
        osm_response = requests.get(f'https://nominatim.openstreetmap.org/?addressdetails=1&q={name_w_plus}&format=json&limit=1&state=British+Columbia').text
        osm_data = json.loads(osm_response)
        if osm_data == []:
            time.sleep(2)
            count += 1
            name = location['localizedValues'][0]['shortName']
            name_w_plus = name.replace(" ", "+")
            osm_response = requests.get(f'https://nominatim.openstreetmap.org/?addressdetails=1&q={name_w_plus}&format=json&limit=1&state=British+Columbia').text
            osm_data = json.loads(osm_response)
            if osm_data == []:
                print("failure")
                exit()
        lat = float(osm_data[0]['lat'])
        lon = float(osm_data[0]['lon'])
        ending_point = [lon, lat]

    

    ors_example_body = {"coordinates":[starting_point,ending_point],"instructions":"false","maneuvers":"false"}

    ors_call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=ors_example_body, headers=ors_headers)

    #print(ors_call.status_code)
    #print(ors_call.text)

    result = json.loads(ors_call.text)

    try:
       result =  int(result["routes"][0]["summary"]["duration"]) #returns duration in seconds
    except KeyError:
        print(ors_call.status_code)
        print(ors_call.text)
        output_data[name] = None

    time.sleep(2)


with open(f'bad-sports.pickle', 'wb') as f:
    pickle.dump(output_data, f, pickle.HIGHEST_PROTOCOL)
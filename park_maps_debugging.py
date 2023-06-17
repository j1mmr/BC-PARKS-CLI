import json
import requests
import pickle
import time

# import secret keys
with open("auth.json", "r") as file:
    data = json.load(file)

# set up ors calls
ors_auth = data["ors_auth"]
ors_headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248f82140ae37c1474981d918825f667a52',
    'Content-Type': 'application/json; charset=utf-8'
}

def get_coords(address):
    address_converted = address.replace(" ", "%20")
    bc_call = requests.get(f'https://geocoder.api.gov.bc.ca/addresses.json?addressString={address_converted}&locationDescriptor=any&maxResults=3&interpolation=adaptive&echo=true&brief=false&autoComplete=false&setBack=0&outputSRS=4326&minScore=1&provinceCode=BC')
    coordinates_data = json.loads(bc_call.text)
    selection = 1 #nt(input("Which address is correct? (1, 2, or 3):\t"))
    coordinates = coordinates_data["features"][selection-1]["geometry"]["coordinates"]
    #print(coordinates)
    return coordinates



def get_duration(startPoint, endPoint):
    ors_example_body = {"coordinates":[startPoint,endPoint],"instructions":"false","maneuvers":"false"}

    ors_call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=ors_example_body, headers=ors_headers)

    #print(ors_call.status_code)
    #print(ors_call.text)

    result = json.loads(ors_call.text)
    try:
        dur = result["routes"][0]["summary"]["duration"] #returns duration in seconds
    except:
        dur = 0
        
    return dur    
def duration_string(duration):
    minutes = duration // 60
    minutes = round(minutes)
    hours = minutes // 60

    minutes %= 60

    return f"{hours} hours and {minutes} minutes"

startPoint = get_coords("4538 Angus Drive, Vancouver, BC")
startPoint_flipped = [startPoint[1], startPoint[0]]
with open("locationData-2023-06-15-2.pickle", "rb") as file:
    locations = pickle.load(file)

for park_id in locations:
    endPoint = locations[park_id][1]
    endPoint_flipped = [endPoint[1], endPoint[0]]

    duration = get_duration(startPoint, endPoint)

    print(f"Duration: {duration_string(duration)}")
    time.sleep(2)

'''

'''
import requests
import datetime
import json
import pickle

# ------------------- Prompt user for location data-------------------
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


#--------------------------------- Get duration of trip -------------------------------
def get_duration (end_point):
    global start_point
    duration = get_duration(start_point, end_point)
    return duration

start_date = '2023-06-30' #input("Enter start date (YYYY-MM-DD):\t")
end_date = '2023-07-02' #input("Enter end date (YYYY-MM-DD):\t")

def duration_string(duration):
    minutes = duration // 60
    minutes = round(minutes)
    hours = minutes // 60

    minutes %= 60

    return f"{hours} hours and {minutes} minutes"


# set up ors calls
ors_auth = data["ors_auth"]
ors_headers = {
    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
    'Authorization': '5b3ce3597851110001cf6248f82140ae37c1474981d918825f667a52',
    'Content-Type': 'application/json; charset=utf-8'
}


#set up address to coordinates system
def get_coords(address):
    address_converted = address.replace(" ", "%20")
    bc_call = requests.get(f'https://geocoder.api.gov.bc.ca/addresses.json?addressString={address_converted}&locationDescriptor=any&maxResults=3&interpolation=adaptive&echo=true&brief=false&autoComplete=false&setBack=0&outputSRS=4326&minScore=1&provinceCode=BC')
    coordinates_data = json.loads(bc_call.text)
    '''
    option1 = coordinates_data["features"][0]["properties"]["fullAddress"]
    option2 = coordinates_data["features"][1]["properties"]["fullAddress"]
    option3 = coordinates_data["features"][2]["properties"]["fullAddress"]
    print(f"#1\t{option1}")
    print(f"#2\t{option2}")
    print(f"#3\t{option3}")
    '''
    selection = 1 #nt(input("Which address is correct? (1, 2, or 3):\t"))
    
    coordinates = coordinates_data["features"][selection-1]["geometry"]["coordinates"]
    return coordinates

def get_duration(end_point):
    global start_point
    ors_example_body = {"coordinates":[start_point,end_point],"instructions":"false","maneuvers":"false"}

    ors_call = requests.post('https://api.openrouteservice.org/v2/directions/driving-car', json=ors_example_body, headers=ors_headers)

    #print(ors_call.status_code)
    #print(ors_call.text)

    result = json.loads(ors_call.text)

    try:
       result =  int(result["routes"][0]["summary"]["duration"]) #returns duration in seconds
    except KeyError:
        print(ors_call.status_code)
        print(ors_call.text)
        return float("inf")
    return result

def duration_string(duration):
    minutes = duration // 60
    minutes = round(minutes)
    hours = minutes // 60

    minutes %= 60

    return f"{hours} hours and {minutes} minutes"

start_point = get_coords("4538 angus drive vancouver")#input("Enter starting address:\t"))
print(start_point)


#--------------------------------- Get location of park -------------------------------
with open(r'locationData-2023-06-15-2.pickle', 'rb') as handle:
    location_data = pickle.load(handle)
            

def location_finder(park):
    global location_data
    try:
        return location_data[int(park)]
    except KeyError:
        raise KeyError(f"Location data not found for park: {park}")


current_time = datetime.datetime.utcnow().isoformat() + 'Z'

cart_response = requests.get('https://camping.bcparks.ca/api/cart')
cart_data = json.loads(cart_response.text)
cart_uid = cart_data["cartUid"]
cart_transaction_uid = cart_data["createTransactionUid"]



norther_url = f'https://camping.bcparks.ca/api/availability/map?mapId=-2147483550&bookingCategoryId=0&equipmentCategoryId=-32768&subEquipmentCategoryId=-32768&cartUid={cart_uid}&cart_transaction_uid={cart_transaction_uid}&bookingUid=9b7d0ec4-7f50-43cc-b7b9-a223958b49c1&startDate={start_date}&endDate={end_date}&getDailyAvailability=false&isReserving=true&filterData=[]&boatLength=null&boatDraft=null&boatWidth=null&partySize=1&numEquipment=1&seed={current_time}'
costal_url = f'https://camping.bcparks.ca/api/availability/map?mapId=-2147483549&bookingCategoryId=0&equipmentCategoryId=-32768&subEquipmentCategoryId=-32768&cartUid={cart_uid}&cart_transaction_uid={cart_transaction_uid}&bookingUid=9b7d0ec4-7f50-43cc-b7b9-a223958b49c1&startDate={start_date}&endDate={end_date}&getDailyAvailability=false&isReserving=true&filterData=[]&boatLength=null&boatDraft=null&boatWidth=null&partySize=1&numEquipment=1&seed={current_time}'
island_url = f'https://camping.bcparks.ca/api/availability/map?mapId=-2147483552&bookingCategoryId=0&equipmentCategoryId=-32768&subEquipmentCategoryId=-32768&cartUid={cart_uid}&cart_transaction_uid={cart_transaction_uid}&bookingUid=9b7d0ec4-7f50-43cc-b7b9-a223958b49c1&startDate={start_date}&endDate={end_date}&getDailyAvailability=false&isReserving=true&filterData=[]&boatLength=null&boatDraft=null&boatWidth=null&partySize=1&numEquipment=1&seed={current_time}'
interior_url = f'https://camping.bcparks.ca/api/availability/map?mapId=-2147483551&bookingCategoryId=0&equipmentCategoryId=-32768&subEquipmentCategoryId=-32768&cartUid=f{cart_uid}&cart_transaction_uid={cart_transaction_uid}&bookingUid=9b7d0ec4-7f50-43cc-b7b9-a223958b49c1&startDate={start_date}&endDate={end_date}&getDailyAvailability=false&isReserving=true&filterData=[]&boatLength=null&boatDraft=null&boatWidth=null&partySize=1&numEquipment=1&seed={current_time}'
regions = []

northern_text = requests.get(norther_url).text
northern_data = json.loads(northern_text)
regions.append(northern_data)

costal_text = requests.get(costal_url).text
costal_data = json.loads(costal_text)
regions.append(costal_data)

island_text = requests.get(island_url).text
island_data = json.loads(island_text)
regions.append(island_data)

interior_text = requests.get(interior_url).text
interior_data = json.loads(interior_text)
regions.append(interior_data)

region_distances = []

for regional_list in regions:
    temp_list = []
    park_statuses = regional_list['mapLinkAvailabilities']
    for park, status in park_statuses.items():
        if status == [0]:
            try:
                current_park_location = location_finder(park)
            except:
                continue
            name = current_park_location[0]
            location = current_park_location[1]
            drive_length = get_duration(location) #lat and long
            temp_list.append([name, location])
            region_distances.append(temp_list)
            print(f"{name} is available at {drive_length/60} minutes away")
            
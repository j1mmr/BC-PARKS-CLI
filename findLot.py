import requests

def find_parking_lots_in_park(park_name):
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
        // Search for the park by name
        way["name"="{park_name}"]["boundary"="national_park"];
        relation["name"="{park_name}"]["boundary"="national_park"];
    );
    (
        // Find parking lots within the park
        way["amenity"="parking"](area);
        relation["amenity"="parking"](area);
    );
    out geom;
    """

    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        data = response.json()

        if 'elements' in data:
            parking_lots = []
            for element in data['elements']:
                if 'type' in element and element['type'] == 'way':
                    parking_lot_lat = element.get('lat')
                    parking_lot_lon = element.get('lon')
                    parking_lots.append((parking_lot_lat, parking_lot_lon))
                elif 'type' in element and element['type'] == 'relation':
                    for member in element.get('members', []):
                        if 'type' in member and member['type'] == 'way':
                            parking_lot_lat = member.get('lat')
                            parking_lot_lon = member.get('lon')
                            parking_lots.append((parking_lot_lat, parking_lot_lon))

            return parking_lots

        else:
            print(f"No park found with the name '{park_name}' or no parking lots found within the park.")
    else:
        print("Error: Failed to retrieve data from the Overpass API.")

    return []

# Specify the park name
park_name = "Top of the World Provincial Park"

# Call the function to find the parking lots inside the park
parking_lots = find_parking_lots_in_park(park_name)

# Print the coordinates of the parking lots
if parking_lots:
    for parking_lot_coordinates in parking_lots:
        parking_lot_lat, parking_lot_lon = parking_lot_coordinates
        print("Parking Lot Latitude:", parking_lot_lat)
        print("Parking Lot Longitude:", parking_lot_lon)
else:
    print("No parking lots found within the park.")

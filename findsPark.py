import requests
import json

park_name = "Top of the World Provincial Park"

overpass_url = "https://overpass-api.de/api/interpreter"
overpass_query = f"""
[out:json];
(
    // Search for the park by name
    way["name"="{park_name}"]["boundary"="national_park"];
    relation["name"="{park_name}"]["boundary"="national_park"];
);
out geom;
"""

response = requests.get(overpass_url, params={'data': overpass_query})

data = response.json()
print(data)
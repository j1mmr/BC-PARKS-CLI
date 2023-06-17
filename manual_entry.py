import pickle

with open('bad-spots.pickle', 'rb') as file:
    location_data = pickle.load(file)

print(location_data)
for park in location_data:
    print(f"Check:\t{park}:")
    lat = float(input("Latitude:\t"))
    lon = float(input("Longitude:\t"))
    location_data[park]= [lon,lat]

with open('bad-spots-r1.pickle', 'wb') as file:
    pickle.dump(location_data, file)
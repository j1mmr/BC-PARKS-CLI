import pickle

with open('bad-spots-r1.pickle', 'rb') as file:
    location_data = pickle.load(file)

print(location_data)
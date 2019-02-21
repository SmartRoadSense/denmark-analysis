import datetime
import time
import geopy.distance
import numpy as np
import pandas as pd

AGGREGATION_RADIUS = 10


def get_IRI(data):
    return np.average(data.values[3:5])


def get_geographical_distance(lat1, long1, lat2, long2):

    coords_1 = (lat1, long1)
    coords_2 = (lat2, long2)

    return geopy.distance.vincenty(coords_1, coords_2).m


def get_PPE_aggregation(lat, long, data):

    ppe = []
    for index, point in data.iterrows():

        distance = get_geographical_distance(lat, long, point[2], point[1])

        if distance < AGGREGATION_RADIUS:
            #print("distance {0}".format(distance))
            ppe.append(point[0])

    ppe_avg = np.average(ppe)

    return ppe_avg


ppe_data = pd.read_csv("data/denmark-srs-data.csv", delimiter=";")
iri_data = pd.read_csv("data/denmark-iri-data.csv", delimiter=";")

iri_data = iri_data.filter(items=['Distance [m]', 'Latitude', 'Longitude', 'IRI(1)', 'IRI(17)'])
iri_data['AVG IRI'] = iri_data.apply(lambda row: (row['IRI(1)'] + row['IRI(17)'])/2, axis=1)
iri_data.to_csv('data/denmark-avgiri-data.csv', sep=';', encoding='utf-8')

print(ppe_data.head())
print(iri_data.head())

output = pd.DataFrame(columns=['distance', 'latitude', 'longitude', 'iri', 'ppe'])
start = time.time()

for index, row in iri_data.iterrows():

    ppe = get_PPE_aggregation(row[1], row[2], ppe_data)
    output = output.append({'distance': row[0], 'latitude': row[1], 'longitude': row[2], 'iri': row[5], 'ppe': ppe},
                           ignore_index=True)

    # ETA stats
    end = time.time()
    elapsed_time = end - start
    iteration = index + 1
    seconds = (elapsed_time) * (len(iri_data) / iteration)
    completion_percentage = (iteration * 100)/len(iri_data)
    eta = str(datetime.timedelta(seconds=(seconds-elapsed_time)))
    print("\r{3}/{4} Time for completion {0} - ETA: {1} - Completion {2:.2f}%".format(str(datetime.timedelta(seconds=seconds)), eta, completion_percentage, index, len(iri_data)), end='')

print('completed')
output.to_csv('data/srs-iri-data.csv', sep=';', encoding='utf-8')
print(np.corrcoef(output['iri'], output['ppe']))

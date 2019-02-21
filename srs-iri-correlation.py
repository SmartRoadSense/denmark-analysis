import pandas as pd
import numpy as np
import geopy.distance

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
            print("distance {0}".format(distance))
            ppe.append(point[0])

    ppe_avg = np.average(ppe)

    return ppe_avg, distance


ppe_data = pd.read_csv("data/denmark-srs-data.csv", delimiter=";")
iri_data = pd.read_csv("data/denmark-iri-data.csv", delimiter=";")

print(ppe_data.head())

iri_data = iri_data.filter(items=['Distance [m]', 'Latitude', 'Longitude', 'IRI(1)', 'IRI(17)'])
print(iri_data.head())

output = pd.DataFrame(columns=['distance', 'latitude', 'longitude', 'iri', 'ppe'])

for index, row in iri_data.iterrows():
    print("{0}/{1}".format(index, len(iri_data)))
    iri = get_IRI(row)
    ppe = get_PPE_aggregation(row[1], row[2], ppe_data)

    output = output.append({'distance': row[0], 'latitude': row[1], 'longitude': row[2], 'iri': iri, 'ppe': ppe},
                           ignore_index=True)
    if index > 3:
        break


output.to_csv('data/srs-iri-data.csv', sep=';', encoding='utf-8')

print(output['iri'])
print(output['ppe'])

print(np.corrcoef(output['iri'], output['ppe']))

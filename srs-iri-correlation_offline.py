import numpy as np
import pandas as pd


data = pd.read_csv("data/srs-iri-data.csv", delimiter=";")
data1 = data[['iri', 'ppe']]
print(data1.head())

print(data1.corr())
#print(np.corrcoef([data['iri'], data['ppe']]))

import folium as fl
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def plottagem_data(dataset):
    min_lat = dataset['Latitude'].min()
    max_lat = dataset['Latitude'].max()
    min_long = dataset['Longitude'].min()
    max_long = dataset['Longitude'].max()
    map = fl.Map(location=[(min_lat+max_lat)/2,(min_long+max_long)/2],
                     tiles="Stamen Terrain", zoom_start=10)
    for element in dataset.tail(50).values:
        fl.Marker([element[1],element[2]],
                  popup=dt.datetime.fromtimestamp(int(element[0])).strftime("{%d-%m-%Y %H:%M:%S}'")
                  ).add_to(map)

    map.save('C:\\Users\Livnick\Documents\dadosFocos\focosMS001.html')

def df_normalizer(dataset):
    dataset = dataset.fillna(0)
    dataset = dataset.loc[~(dataset == 0).all(axis=1)]
    min_max_scaler = MinMaxScaler()
    data = min_max_scaler.fit_transform(dataset)
    return pd.DataFrame(data, columns=dataset.columns)


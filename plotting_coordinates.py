import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from geopandas import GeoDataFrame
import folium

df = pd.read_csv("mumbai_lat_longs.csv", delimiter=',', skiprows=0, low_memory=False)

points = zip(df['lat'], df['long'])

m = folium.Map(location=[19.075983, 72.877655],
           zoom_start=12)

for point in points:
    print(list(point))
    folium.Marker(location=point, fill_color='#43d9de', radius=8).add_to(m)


m.save('map.html')



# #this is a simple map that goes with geopandas
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
# gdf.plot(ax=world.plot(figsize=(10, 6)), marker='o', color='red', markersize=15)

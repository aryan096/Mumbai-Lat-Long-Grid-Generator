import fiona
import shapefile
import shapely.geometry
import math
import csv

## LAT, LONG, CALCULATIONS 

EARTH = 6378.137
PI = math.pi

def remove_out_of_bounds(lat_longs):
    with fiona.open("shapefile/mumbai_shapefile.shp") as fiona_collection:

        new_lat_longs = []

        for index, coord in enumerate(lat_longs):
            point = shapely.geometry.Point((coord[1], coord[0]))
            
            # In this case, we'll assume the shapefile only has one record/layer (e.g., the shapefile
            # is just for the borders of a single country, etc.).
            for shapefile_record in fiona_collection:
                # Use Shapely to create the polygon
                shape = shapely.geometry.asShape(shapefile_record['geometry'] )

                if point.within(shape):
                    print(index)
                    new_lat_longs.append((coord[1], coord[0]))
                    break
        
        return new_lat_longs

def get_new_latitude(old_lat):
    m = (1 / ((2 * PI / 360) * EARTH)) / 1000
    new_lat = old_lat + (400 * m)
    return new_lat
    
def get_new_longitude(old_long, lat):
    m = (1 / ((2 * PI / 360) * EARTH)) / 1000
    new_long = old_long + (400 * m) / math.cos(lat * (PI / 180))
    return new_long


def get_all_valid_longitudes(lat):
    start_longitude = 72.743437
    end_longitude = 73.089732
    curr_longitude = start_longitude

    lat_longs = []

    while curr_longitude < end_longitude:
        lat_longs.append((lat, curr_longitude))
        curr_longitude = get_new_longitude(curr_longitude, lat)

    return lat_longs

def get_all_valid_lat_longs():
    start_latitude = 18.879326
    end_latitude = 19.302395

    curr_latitude = start_latitude

    all_lat_longs = []

    while curr_latitude < end_latitude:
        lat_longs = get_all_valid_longitudes(curr_latitude)
        all_lat_longs = all_lat_longs + lat_longs
        curr_latitude = get_new_latitude(curr_latitude)

    return remove_out_of_bounds(all_lat_longs)

def main():

    all_lat_longs = get_all_valid_lat_longs()

    with open('mumbai_lat_longs_400.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['long','lat'])
        for lat_long in all_lat_longs:
            csv_out.writerow(lat_long)


if __name__ == "__main__":
    main()



# start_longitude = 72.743437

# end_longitude = 73.089732

# curr_latitude = start_latitude
# curr_longitude = start_longitude

# curr_coordinates = (curr_latitude, curr_longitude)


# with fiona.open("shapefile/mumbai_shapefile.shp") as fiona_collection:

#     # In this case, we'll assume the shapefile only has one record/layer (e.g., the shapefile
#     # is just for the borders of a single country, etc.).
#     for shapefile_record in fiona_collection:
#         # Use Shapely to create the polygon
        
#         shape = shapely.geometry.asShape(shapefile_record['geometry'] )

#         point = shapely.geometry.Point(start_coordinates)

#         if point.within(shape):
#             print('within')
#         else:
#             print('nope')

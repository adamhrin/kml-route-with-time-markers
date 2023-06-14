import argparse

import simplekml
from fastkml import kml
from haversine import haversine
from datetime import datetime, timedelta
from hereutil import here

def get_route_coords(kml_file):
    k = kml.KML()
    with open(kml_file, 'rt', encoding='utf-8') as file:
        doc = file.read()
    # k.from_string(doc)
    k.from_string(doc.encode('utf-8'))
    features = list(k.features())
    folders = list(features[0].features())
    placemarks = list(folders[0].features())
    linestring = placemarks[0].geometry
    coords = [(coord[1], coord[0]) for coord in linestring.coords]
    return coords

def get_marker_coords(coords, total_time, interval):
    total_distance = 0
    for i in range(1, len(coords)):
        total_distance += haversine(coords[i-1], coords[i])
    speed = total_distance / total_time  # speed in km/min
    marker_coords = []
    accumulated_distance = 0
    for i in range(1, len(coords)):
        segment_distance = haversine(coords[i-1], coords[i])
        if accumulated_distance + segment_distance < interval * speed:
            accumulated_distance += segment_distance
        else:
            while accumulated_distance + segment_distance >= interval * speed:
                ratio = (interval * speed - accumulated_distance) / segment_distance
                new_coord = (coords[i-1][0] + ratio * (coords[i][0] - coords[i-1][0]), 
                             coords[i-1][1] + ratio * (coords[i][1] - coords[i-1][1]))
                marker_coords.append(new_coord)
                segment_distance -= interval * speed - accumulated_distance
                accumulated_distance = 0
    return marker_coords

def create_kml_with_markers(route_coords, marker_coords, start_time, interval):
    kml = simplekml.Kml()
    linestring = kml.newlinestring(name="Route", coords=[(c[1], c[0]) for c in route_coords])
    time = datetime.strptime(start_time, '%H:%M')
    for i, coord in enumerate(marker_coords):
        min_from_start = (i+1)*interval
        time = time + timedelta(minutes=interval)
        point = kml.newpoint(name=f"{min_from_start} min ({datetime.strftime(time, '%H:%M')})", coords=[(coord[1], coord[0])])
    kml.save(here("data/output/route_with_time_markers.kml"))


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', type=str, help='kml route input file path')
    parser.add_argument('--goal_time', type=int, help='estimated time it takes to traverse route (in minutes)')
    parser.add_argument('--interval', type=int, default=5, help='interval time (in minutes)')
    parser.add_argument('--start_time', type=lambda s: datetime.strptime(s, '%H:%M').strftime('%H:%M'))
    args = parser.parse_args()

    kml_file = here(args.input_file)  # replace with your kml file
    total_time = args.goal_time  # replace with your total time in minutes
    interval = args.interval  # interval in minutes

    route_coords = get_route_coords(kml_file)
    marker_coords = get_marker_coords(route_coords, total_time, interval)
    create_kml_with_markers(route_coords, marker_coords, args.start_time, interval)

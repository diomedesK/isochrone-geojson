import geojson, sys, json

def generatePoints(target_coords, output_path):
    points = []

    # Geojson stores coordinates in a longitude-latitude scheme, in contrast to the most common (Google Maps for example) latitude-longitude,
    # hence the inversion

    for coord in target_coords:
        lat, lon = coord
        point = geojson.Point(coordinates=(lon, lat))
        points.append(point)

    generatedFeature = geojson.FeatureCollection(features=[geojson.Feature(geometry=geojson.MultiPoint(points))])

    with open(output_path, "w") as file:
        geojson.dump(generatedFeature, file)

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python script.py <coordinates-json> <output-path> ')
        sys.exit(1)

    with open(sys.argv[1], "r") as file:
        target_coords = [tuple(entry["coords"]) for entry in json.load(file).get("coordinates")]

    generatePoints(target_coords, sys.argv[2])
    print(f"Generated points file at {sys.argv[2]}")

# MAKE A MULTIPOLYGON FOR EACH UNITY FOR EACH KEY DISTANCE [N FOR N IN RANGE(1, 11) IF N % 2 == 0] WITH A UNIQUE COLOR
import geojson, requests, time
import concurrent.futures

def requestIsochrone(apiURL, payload):
    response = requests.post(apiURL, json=payload)
    return response

def generateIsochrones(target_coords, minutes_time, costing, output_path):
    ISOCHRONE_API = "https://valhalla1.openstreetmap.de/isochrone"

    default_props = {}

    def makePayload(lat, lon):
        payload = {
                # https://valhalla.github.io/valhalla/api/isochrone/api-reference/
                "locations": [{ "lat": lat, "lon": lon }], # set empty dict for allowing dynamic changes; valhalla api doesnt support multiple location fetching
                "costing": costing,
                "contours": [
                    {
                        "time": minutes_time,
                        "color": "ff0000"
                        }
                    ],
                "polygons": True
                }

        return payload

    polygons_to_be_added = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        left_futures: list[concurrent.futures.Future] = []

        future2payload = {}

        print(f"Starting sequence of {len(target_coords)} requests, it may take a bit to conclude...")
        for count, coord in enumerate(target_coords):
            payload = makePayload(coord[0], coord[1])
            future = executor.submit( requestIsochrone, apiURL=ISOCHRONE_API, payload=payload )
            future2payload[future] = payload

            left_futures.append(future)

        while True:
            failed_futures = [f for f in left_futures if f.result().status_code != 200 ]
            if(len(failed_futures) == 0):
                break

            print(f"{len(failed_futures)}/{len(target_coords)} have failed (429, too many requests); retrying...")

            for future in failed_futures:
                retry_future = executor.submit( requestIsochrone, apiURL=ISOCHRONE_API, payload=future2payload[future])
                future2payload[retry_future] = future2payload[future]

                left_futures.remove(future)
                future2payload.pop(future)

                left_futures.append(retry_future)

        for future in left_futures:
            response  = future.result()
            if(response.status_code == 200):
                rjson = response.json()
                polygon_cords = rjson.get("features")[0].get("geometry").get("coordinates")
                polygon = geojson.Polygon( polygon_cords )
                polygons_to_be_added.append(polygon)

    generatedFeature = geojson.FeatureCollection(
            [
                geojson.Feature( properties=default_props, geometry=geojson.MultiPolygon(polygons_to_be_added))
            ]
        )

    with open(output_path, "w") as file:
        geojson.dump(generatedFeature, file)

    return True


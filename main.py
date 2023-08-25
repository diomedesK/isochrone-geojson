import argparse, datetime, json, os
import isochrone_maker, point_maker

import time

def main():
    if(not os.path.exists("./generated/")):
        os.mkdir("./generated/")

    parser = argparse.ArgumentParser(description="Generate isochrones for target coordinates.")
    parser.add_argument("input_file", help="Path to the input JSON file containing target coordinates")
    parser.add_argument("--prefix", help="Output prefix for generated files")
    parser.add_argument("--costing", help="The costing (moving mean) used (defaults to motorcycle)", default="motorcycle")
    parser.add_argument("--minute", help="Trip minutes", default=None, type=int)
    parser.add_argument("--minutes", help="Generate isochrones up to N minute", default=10, type=int)

    args = parser.parse_args()

    target_coords = []

    with open(args.input_file, "r") as file:
        target_coords = [tuple(entry["coords"]) for entry in json.load(file).get("coordinates")]

    time_range = [args.minute]
    if(args.minute == None):
        time_range = [n for n in range(1, (args.minutes + 1) ) if n % 2 == 0]

    current_datestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    print(f"Time range is {time_range}")
    for time in time_range:
        if args.prefix:
            outputp = f"./generated/{args.prefix}_{args.costing}_{int(time)}min.geojson"
        else:
            outputp = f"./generated/output_{args.costing}_{int(time)}min_{current_datestamp}.geojson"

        try:
            isochrone_maker.generateIsochrones(target_coords, time, args.costing, outputp)
            print(f"Generated isochrones for a {time} minute(s) {args.costing} trip saved at {outputp}")
        except Exception:
            raise Exception

    if args.prefix:
        points_filepath = f"./generated/{args.prefix}_points.geojson" 
    else:
        points_filepath = f"./generated/output_{current_datestamp}_points.geojson" 

    point_maker.generatePoints(target_coords, points_filepath)
    print(f"Generated points file at {points_filepath}")

if __name__ == "__main__":
    main()
    time.sleep(5)


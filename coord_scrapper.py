#pyright: reportGeneralTypeIssues = false
#pyright: reportOptionalMemberAccess = false

from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup

import geopy, requests, concurrent.futures, time, json, re, sys

def fetch_coordinates(cep):
    if bool(re.match("^\\d{5}-?\\d{3}$", cep)) == False:
        return None
    
    print(f"Fetching {cep}")
    geolocator = Nominatim(user_agent="geolocalização")
    try:
        location = geolocator.geocode(cep, timeout=5)
        if location:
            return {"cep": cep, "coords": (location.latitude, location.longitude)}
    except geopy.exc.GeocoderRateLimited:
        print("Geocoder rate limit. Sleeping for 5 seconds.")
        time.sleep(5)
    except Exception:
        pass
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <URL> <output?>")
        sys.exit(1)

    url = sys.argv[1]
    expected_domain = "https://www.catalogosofertas.com.br"
    if not url.startswith(expected_domain):
        print(f"Invalid URL. Please provide a URL from '{expected_domain}'.")
        sys.exit(1)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    locations = soup.select(".location")
    ceps = [location.select_one(".txt-title").get_text().split(" ")[0] for location in locations if location.select_one(".txt-title")]

    ceps2coords = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        time.sleep(5)
        futures = list(executor.map(fetch_coordinates, ceps))

    for future in futures:
        if future:
            ceps2coords.append(future)

    jsonified = {
            "coordinates": ceps2coords
        }

    outputp = sys.argv[2] if len(sys.argv) > 2 else "coordinates.json"
    with open(outputp, "w") as file:
        json.dump(jsonified, file)

    print(f"Outputed to {outputp}")

# isochrone-geojson
A set of utilities for generating .geojson files representing isochrones for a given set of coordinates.

### How to use it

You may input any JSON file that follows the contract:
```json
{
  "coordinates": [
        "coords": ["latitude", "longitude"]
    ]
}
```

That is, a JSON which has a root element named "coordinates" and which holds an array of "coords" containing both a latitude and a longitude.

Then execute the ```main.py``` file
``` text
usage: main.py [-h] [--prefix PREFIX] [--costing COSTING] [--minute MINUTE] [--minutes MINUTES] input_file

Generate isochrones for target coordinates.

positional arguments:
  input_file         Path to the input JSON file containing target coordinates

options:
  -h, --help         show this help message and exit
  --prefix PREFIX    Output prefix for generated files
  --costing COSTING  The costing (moving mean) used (defaults to motorcycle)
  --minute MINUTE    Trip minutes
  --minutes MINUTES  Generate isochrones up to N minute
```

``` shell
$ python main.py ./coordinates/pague-menos.json --minute 10 --prefix pague-menos --costing pedestrian
```

Visit the [valhalla docs](https://valhalla.github.io/valhalla/api/turn-by-turn/api-reference/#costing-models) for more info about the allowed costing options, but probably you would like
- pedestrian
- bicycle
- auto
- motorcycle


### Generating coordinates

You may input the coordinates manually if they are only a few, but for my case I wrote the ```coord-scrapper.py``` script . It works over the website [https://www.catalogosofertas.com.br/], which contains some nice info about the addresses of unities of franchises all over Brazil.
For example:
```shell
$ python https://www.catalogosofertas.com.br/lojas/bradesco/localizacoes/rio-de-janeiro bradesco.json
# will generate coordinates for the outlets of the Bradesco bank in the city of Rio and output to ./bradesco.json
```

Just browse the website and find the page that you need.

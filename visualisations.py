
###
# Create maps and plots of data and results
# that populate the md or html outputs
# that we will share publicly
#

import geopandas as gpd
from keplergl import KeplerGl

# Import parks
parks = gpd.read_file("data/Parks_in_King_County___park_area.geojson")

# Create a map
config = {
  "version": "v1",
  "config": {
    "mapState": {
      "bearing": 0,
      "dragRotate": False,
      "latitude": 47.5,
      "longitude": -121.8,
      "pitch": 0,
      "zoom": 8,
      "isSplit": False
    },
    "mapStyle": {
      "styleType": "light",
      "visibleLayerGroups": {
        "label": True,
        "road": False,
        "border": False,
        "building": False,
        "water": True,
        "land": True,
        "3d building": False
      },
    }
  }
}
# per https://docs.kepler.gl/docs/keplergl-jupyter#5.-save-and-load-config
# a full config can supposedly be exported from the viewer
# using the {} icon in the sidebar 
# but I dont see that option in my viewer

# Render the map and export it to the outputs folder
map=KeplerGl(height=500, config=config)
map.add_data(data=parks, name='Parks in King Co')
map.save_to_html(file_name="outputs/kingco_parks.html", config=config)

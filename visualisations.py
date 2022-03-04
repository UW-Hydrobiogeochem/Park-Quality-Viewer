
###
# Create maps and plots of data and results
# that populate the md or html outputs
# that we will share publicly
#

import geopandas as gpd
from keplergl import KeplerGl
import plotly.express as px
import plotly.graph_objects as go

# Import parks environ
parks_environ = gpd.read_file("outputs/parks_environ.geojson")

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

# NOTE: this map is for the original data brought in with parks data layer.
# TODO: need to figure out how to use data from parks_environ in kepler 
# Render the map and export it to the outputs folder
map=KeplerGl(height=500, config=config)
map.add_data(data=parks, name='Parks in King Co')
map.save_to_html(file_name="outputs/kingco_parks.html", config=config)

##############################################
# ------------- Scatter Plots ---------------
##############################################

# compare park demographic data against park environmental quality data
fig1 = px.scatter(parks_environ,x='walk_totalPop',y='pm25areaAvg',color='walk_pct_NotWhite', hover_data=['SITENAME'])
fig1.show()
fig2 = px.scatter(parks_environ,x='walk_totalPop',y='no2areaAvg',color='walk_pct_NotWhite', hover_data=['SITENAME'])
fig2.show()

# water quality
parks_environ_plot = parks_environ[pd.notna(parks_environ['CatCodeNum'])]
fig = px.scatter(parks_environ_plot,x='walk_totalPop',y='walk_pct_NotWhite' ,color='CatCodeNum', 
    hover_data=['SITENAME'],color_continuous_scale=px.colors.sequential.Sunsetdark)
fig.show()
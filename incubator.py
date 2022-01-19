
# Here is where the code lives

# Motivation: 
# Green and blue spaces in urban areas provide refuge against hot temperatures
# Areas in King County impacted by air and water pollution
# Important to understand benefits and risks associated with existing and planned spaces for climate adaptation

# Import Libraries
# not sure what happened, but when re-ran code with 'pip install geopandas' got SyntaxError
# tried downloading and installing pip. Didn't fix problem
# code does run without those two lines, with just importing geopandas and reading data
#$ python get-pip.py
#pip install geopandas # not sure if I have to do this eash time or only once
from turtle import title
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt
import pandas as pd
import rtree #needed for clipping in geopandas

# ------ Import Data -----------------
# polygons representing parks + environmental layer (grid?)
# ideally, enviornmental data is at higher resolution than park data
# data will come in different projections --> will need to reconcile
# geopandas.org for importing shapefiles
# https://geopandas.org/en/stable/docs/user_guide/io.html
# next step (jan 5): Becca practice import with smaller data. json file of King County parks that Spencer has al

# King County Data
parks = gpd.read_file("data/Parks_in_King_County___park_area.geojson")
water = gpd.read_file("data/Open_water_for_King_County_and_portions_of_adjacent_counties___wtrbdy_area.geojson")

# WA DEQ polluted water bodies
fiona.listlayers("data/WQ_ENV_WQAssessmentCurrent.gdb")
# ['WQ_ENV_WQAssessmentCurrent_WQAssessmentCurrent_305b',
#  'WQ_ENV_WQAssessmentCurrent_WQAssessmentCurrent_303d',
#  'WQ_ENV_WQAssessmentCurrent_WQACurrent303d',
#  'WQ_ENV_WQAssessmentCurrent_WQACurrent305b']
water303 = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=2)

# mask
aoi = gpd.read_file("data/King_County_Political_Boundary_(no_waterbodies)___kingco_area.geojson")    
# aoi = gpd.read_file("Data/aoi.geojson")

# census data shape file
blockgroup = gpd.read_file("data/bg10/bg10.shp")
# to do -- clip out area of interest and save a new shp file for working in project
blockgroup.dtypes

# air quality data
pm25 = pd.read_csv("data/CACES_PM25_2015_censusblock.csv")
pm25.dtypes
# to connect with air quality data. Do a merge of the data sets using a code, fips key

# Inspect Data
# look at tabular data
parks.head()
water.head()
water303.head()
aoi.head()
pm25.head()
blockgroup.head()

# ---------- align projections
parks.crs
water.crs
water303.crs
aoi.crs
blockgroup.crs
# note: parks, water, aoi are <Geographic 2D CRS: EPSG:4326>
# note: water303 is <Derived Projected CRS: EPSG:2927>
# note: census block is in NAD83
# convert water 303 data to same crs as parks county park and aoi
water303 = water303.to_crs(4326)
blockgroup = blockgroup.to_crs(4326)

# ------- merge air quality data with block group data
blockgroup_int = blockgroup.astype({'GEOID10':"int64"}) # converting data types for merge
blockgroup_int.dtypes
blockgroup_pm25 = blockgroup_int.merge(pm25, left_on='GEOID10', right_on='fips')
#blockgroup_pm25.dtypes

# ---------- clip data with aoi
parks_clip = parks.clip(aoi)
water_clip = water.clip(aoi)
water303_clip = water303.clip(aoi)
blockgroup_pm25_clip = blockgroup_pm25.clip(aoi)

# ----------- make a plot 
base = parks_clip.plot(color="green")
water_clip.plot(ax=base,color="blue")
water303_clip.plot(ax=base,color="red")
aoi.boundary.plot(ax=base,color="black")
plt.show()

# ------ plot air quality data with colors showing air quality
blockgroup_pm25_clip.plot(column='pred_wght',legend='true',
    legend_kwds={'label': "King County Population Weighted PM 2.5 ug/m3 in 2015",
    'orientation': "horizontal"})
plt.show()

# intersect data layers. polygon of parks with envrionmental data
# geopandas.overlay
# https://geopandas.org/en/stable/docs/reference/api/geopandas.clip.html

# summarize environmental data by park
# can work directly on attributes and ignore geometry. e.g. take mean of polygon
# produce a new geofile to display
# can probably do this with pandas...will operate on attributes of polygons
# spatial joins

# visualize results -- not clear what exactly.
# map with park polygons color coded by environmental data measure?
# Ask Scott about visualization step
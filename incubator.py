
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
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt

# ------ Import Data -----------------
# polygons representing parks + environmental layer (grid?)
# ideally, enviornmental data is at higher resolution than park data
# data will come in different projections --> will need to reconcile
# geopandas.org for importing shapefiles
# https://geopandas.org/en/stable/docs/user_guide/io.html
# next step (jan 5): Becca practice import with smaller data. json file of King County parks that Spencer has al

# King County Data
parks = gpd.read_file("Data/Parks_in_King_County___park_area.geojson")
water = gpd.read_file("Data/Open_water_for_King_County_and_portions_of_adjacent_counties___wtrbdy_area.geojson")

# WA DEQ polluted water bodies
fiona.listlayers("data/WQ_ENV_WQAssessmentCurrent.gdb")
# ['WQ_ENV_WQAssessmentCurrent_WQAssessmentCurrent_305b',
#  'WQ_ENV_WQAssessmentCurrent_WQAssessmentCurrent_303d',
#  'WQ_ENV_WQAssessmentCurrent_WQACurrent303d',
#  'WQ_ENV_WQAssessmentCurrent_WQACurrent305b']
water303 = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=2)

# mask
aoi = gpd.read_file("Data/aoi.geojson")

# Inspect Data
# look at tabular data
parks.head()
water.head()
water303.head()
aoi.head()

# ---------- align projections
parks.crs
water.crs
water303.crs
aoi.crs
# note: parks, water and aoi are <Geographic 2D CRS: EPSG:4326>
# note: water303 is <Derived Projected CRS: EPSG:2927>
# convert water 303 data to same crs as parks county park and aoi
water303 = water303.to_crs(4326)

# ---------- clip data with aoi
parks_clip = parks.clip(aoi)
water_clip = water.clip(aoi)
water303_clip = water303.clip(aoi)

# ----------- make a plot 
base = parks_clip.plot(color="green")
water_clip.plot(ax=base,color="blue")
water303_clip.plot(ax=base,color="red")
aoi.boundary.plot(ax=base,color="black")
plt.show()

# Clip data to area of interest --> both layers
# clip with a new polygon that is area of interest or bounding box of coordinates
# geopandas.clip
# https://geopandas.org/en/stable/docs/reference/api/geopandas.clip.html
# mask has to be a vector file. Cannot be a bounding box. To use above function.

# intersect data layers. polygon of parks with envrionmental data
# geopandas.overlay
# https://geopandas.org/en/stable/docs/reference/api/geopandas.clip.html

# summarize environmental data by park
# can work directly on attributes and ignore geometry. e.g. take mean of polygon
# produce a new geofile to display
# can probably do this with pandas...will operate on attributes of polygons

# visualize results -- not clear what exactly.
# map with park polygons color coded by environmental data measure?
# Ask Scott about visualization step
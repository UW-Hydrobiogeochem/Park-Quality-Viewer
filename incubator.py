
# Here is where the code lives

# Motivation: 
# Green and blue spaces in urban areas provide refuge against hot temperatures
# Areas in King County impacted by air and water pollution
# Important to understand benefits and risks associated with existing and planned spaces for climate adaptation

# Import Data
# polygons representing parks + environmental layer (grid?)
# ideally, enviornmental data is at higher resolution than park data
# data will come in different projections --> will need to reconcile
# geopandas.org for importing shapefiles
# https://geopandas.org/en/stable/docs/user_guide/io.html


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
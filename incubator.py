
# Here is where the code lives

# Motivation: 
# Green and blue spaces in urban areas provide refuge against hot temperatures
# Areas in King County impacted by air and water pollution
# Important to understand benefits and risks associated with existing and planned spaces for climate adaptation

# Import Libraries
#$ python get-pip.py
#pip install geopandas 
import geopandas as gpd
import fiona
import matplotlib.pyplot as plt
import pandas as pd

# ===============================================
# =========== Import Data =======================
# ===============================================

#------- King County Data
parks = gpd.read_file("data/Parks_in_King_County___park_area.geojson") # confirmed only polygons in this file
water = gpd.read_file("data/Open_water_for_King_County_and_portions_of_adjacent_counties___wtrbdy_area.geojson")
# Area of interest
aoi = gpd.read_file("data/King_County_Political_Boundary_(no_waterbodies)___kingco_area.geojson")    

#--------- WA DEQ polluted water bodies
fiona.listlayers("data/WQ_ENV_WQAssessmentCurrent.gdb")
# ['WQ_ENV_WQAssessmentCurrent_WQAssessmentCurrent_305b', 
#  'WQ_ENV_WQAssessmentCurrent_WQAssessmentCurrent_303d', 
#  'WQ_ENV_WQAssessmentCurrent_WQACurrent303d',
#  'WQ_ENV_WQAssessmentCurrent_WQACurrent305b']
water305Assess = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=0)
water303Assess = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=1)
water303 = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=2)
water305 = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=3)
# ListingNumber                int64
# CategoryCode                object
# ParameterName               object
# MediumName                  object
# ListingWaterbodyName        object
# AssessmentUnitNumber        object
# EnvironmentTypeCode         object
# AssessmentUnitTypeCode      object
# NHDReachCode                object
# NHDFromMeasurePercent      float64
# NHDToMeasurePercent        float64
# GridCellNumber              object
# UnmappableCode              object
# Shape_Length               float64
# Shape_Area                 float64
# water305Assess.groupby('CategoryCode').groups.keys() #'1', '2', '4A', '4B', '4C', '5'
# water303Assess.groupby('CategoryCode').groups.keys() # 5
# water305.groupby('CategoryCode').groups.keys() # '1', '2', '4A', '4B', '4C', '5'
# water303.groupby('CategoryCode').groups.keys() # 5
# water305Assess.shape #(27989, 16)
# water305.shape #(27989, 16)
# water305Assess.groupby('MediumName').groups.keys() # ['Habitat', 'Other', 'Sediment', 'Tissue', 'Water']
# water305Assess.groupby('EnvironmentTypeCode').groups.keys() # ['Freshwater', 'Marine']
# ----- using water305Assess becuase I think this is the more recent data than water 305

# --------census data shape file
# blockgroup = gpd.read_file("data/bg10/bg10.shp")
block = gpd.read_file("data/block10/block10.shp")

# --------air quality data
# pm25 = pd.read_csv("data/CACES_PM25_2015_censusblock.csv")
pm25 = pd.read_csv("data/pm25block_wa_2015.csv")
# pm25.dtypes
no2 = pd.read_csv("data/no2block_wa_2015.csv")

######################################
# ---------- align projections ------
######################################
# need to chose crs that is projected to make area calculations
# going with EPSG 2927, Unit: US survey foot
# parks.crs
# water.crs
# water303.crs
# aoi.crs
# block.crs
# note: king country parks Projection: State Plane* 
#       Zone: 5601  (Washington State Plane North; FIPS Zone 4601) Datum: HPGN Units: feet
# note: parks, water, aoi are <Geographic 2D CRS: EPSG:4326> according to crs command
# note: water303 is <Derived Projected CRS: EPSG:2927>
# note: census block is in NAD83
parks = parks.to_crs(2927)
water = water.to_crs(2927)
aoi = aoi.to_crs(2927)
block = block.to_crs(2927)
# crs conversion does not change data values. only changes geometries

#####################################################
# ---------- Align, filter, merge, clip data  ------
#####################################################

# ---------- filter water quality data:
# CategoryCode = 4A, 4B, 4C or 5
# ParamterName = toxic list
# MediumName = water
# EnvironmentTypeCode = freshwater
water305Assess_temp = water305Assess[(water305Assess['MediumName']=='Water')&
    (water305Assess['EnvironmentTypeCode']=='Freshwater')&
    ((water305Assess['CategoryCode']=='4A')|(water305Assess['CategoryCode']=='4B')|
    (water305Assess['CategoryCode']=='4C')|(water305Assess['CategoryCode']=='5'))]
water305Assess_temp.groupby('ParameterName').groups.keys()
# ["4,4'-DDD", "4,4'-DDE", "4,4'-DDT", 'Aldrin', 'Aldrin/Dieldrin', 'Ammonia-N', 
# 'Arsenic', 'Bacteria', 'Chloride', 'Chlorine', 'Chlorpyrifos', 'Copper', 
# 'DDT (and metabolites)', 'Diazinon', 'Dieldrin', 'Dioxin', 'Dissolved Oxygen', 
# 'Endosulfan', 'Fish And Shellfish Habitat', 'Hexachlorobenzene', 'Instream Flow', 
# 'Invasive Exotic Species', 'Lead', 'Mercury', 'Silver', 'Temperature', 'Total Dissolved Gas', 
# 'Total Nitrogen', 'Total Phosphorus', 'Turbidity', 'Water Column Bioassay', 'Zinc', 'pH']
toxic = ["4,4'-DDD", "4,4'-DDE", "4,4'-DDT", 'Aldrin', 'Aldrin/Dieldrin',  
    'Arsenic', 'Bacteria', 'Chlorpyrifos', 'DDT (and metabolites)', 'Diazinon', 
    'Dieldrin', 'Dioxin', 'Endosulfan', 'Hexachlorobenzene', 'Lead', 'Mercury', 'Silver']
water305Assess_toxic_water = water305Assess_temp[water305Assess_temp.ParameterName.isin(toxic)]
# CategoryCode = 4A, 4B, 4C or 5
# ParamterName = toxic list
# MediumName = tissue
# EnvironmentTypeCode = freshwater
water305Assess_temp = water305Assess[(water305Assess['MediumName']=='Tissue')&
    (water305Assess['EnvironmentTypeCode']=='Freshwater')&
    ((water305Assess['CategoryCode']=='4A')|(water305Assess['CategoryCode']=='4B')|
    (water305Assess['CategoryCode']=='4C')|(water305Assess['CategoryCode']=='5'))]
water305Assess_temp.groupby('ParameterName').groups.keys()
# ['2,3,7,8-TCDD (Dioxin)', '2,3,7,8-TCDD TEQ', "4,4'-DDD", "4,4'-DDE", "4,4'-DDT", 
# 'Aldrin', 'Alpha-BHC', 'Arsenic, Inorganic', 'Chlordane', 'DDT (and metabolites)', 
# 'Dieldrin', 'Dioxin', 'Heptachlor Epoxide', 'Hexachlorobenzene', 'Mercury', 
# 'Polychlorinated Biphenyls (PCBs)', 'Total Chlordane', 'Toxaphene']
# all these chemicals are toxic
water305Assess_toxic_tissue = water305Assess_temp
# note: sediment data are not for chemicals. Just say assays were conducted.

# ------- merge air quality data with census block group data
block_int = block.astype({'GEOID10':"int64"}) # converting data types for merge
# block_int.dtypes
block_pm25 = block_int.merge(pm25, left_on='GEOID10', right_on='block_fip')
block_no2 = block_int.merge(no2, left_on='GEOID10', right_on='block_fip')

# ---------- clip data with aoi
#parks_clip = parks.clip(aoi)
parks_clip = parks # getting error when clipping, skip clip for now
water_clip = water.clip(aoi)
water305Assess_toxic_water_clip = water305Assess_toxic_water.clip(aoi)
water305Assess_toxic_tissue_clip = water305Assess_toxic_tissue.clip(aoi)
block_pm25_clip = block_pm25.clip(aoi)
block_no2_clip = block_no2.clip(aoi)

############################################
# ---------- make plots of data -----------
############################################

# ----------- make a plot of parks and water
base = parks_clip.plot(color="green")
water_clip.plot(ax=base,color="blue")
water305Assess_toxic_water_clip.plot(ax=base,color="red")
water305Assess_toxic_tissue_clip.plot(ax=base,color="orange")
aoi.boundary.plot(ax=base,color="black")
plt.show()

# ------ plot pm25 quality data with colors showing air quality
block_pm25_clip.plot(column='pred15',legend='true',
    legend_kwds={'label': "King County PM 2.5 ug/m3 in 2015",
    'orientation': "horizontal"})
plt.show()

########################################################################
# -------- intersect data layers to get environmental data at each park
########################################################################

#-------------------------
# ------ air quality data 
#-------------------------
pm25_park_intersect = parks_clip.overlay(block_pm25_clip,how='intersection')
pm25_park_intersect.dtypes
# parks_clip['OBJECTID'].is_unique # true = ID is applied to each park
# pm25_park_intersect['OBJECTID'].is_unique # false = parks have multiple air quality data
# parks_clip['SHAPE_Area'].is_unique # true
# pm25_park_intersect['SHAPE_Area'].is_unique # false...shape area is just the value of whole park carried forward
no2_park_intersect = parks_clip.overlay(block_no2_clip,how='intersection')

# ------------calculated area-averaged values for enviornmental data for each park
# example: (A1*E1 + A2*E2)/(A1+A2)
# find area of each intersection and join to the intersect object
pm25_park_intersect = pm25_park_intersect.join(pm25_park_intersect.area.to_frame(name='intersect_Area'))
# pm25_park_intersect.dtypes
no2_park_intersect = no2_park_intersect.join(no2_park_intersect.area.to_frame(name='intersect_Area'))

# multiply interesect area by air quality value for that area
pm25area = pm25_park_intersect['intersect_Area'] * pm25_park_intersect['pred15']
no2area = no2_park_intersect['intersect_Area'] * no2_park_intersect['pred15']

# join this multiplied value to the intersect object
pm25_park_intersect = pm25_park_intersect.join(pm25area.to_frame(name='pm25area'))
no2_park_intersect = no2_park_intersect.join(no2area.to_frame(name='no2area'))

# sum the multiplied values that exist within a given park and append to a new park object
pm25_park_areasum = pm25_park_intersect.groupby('OBJECTID')['pm25area'].sum()
no2_park_areasum = no2_park_intersect.groupby('OBJECTID')['no2area'].sum()
pm25_park = parks_clip.merge(pm25_park_areasum,left_on='OBJECTID', right_on='OBJECTID')
no2_park = parks_clip.merge(no2_park_areasum,left_on='OBJECTID', right_on='OBJECTID')
# divide sum of multiplied values by total park area to get area weighted average
pm25areaAvg = pm25_park['pm25area'].divide(pm25_park['SHAPE_Area'])
no2areaAvg = no2_park['no2area'].divide(no2_park['SHAPE_Area'])
# append area weighted averages to a new park object
parks_environ = parks_clip.join(pm25areaAvg.to_frame(name='pm25areaAvg'))
parks_environ = parks_environ.join(no2areaAvg.to_frame(name='no2areaAvg'))

# visualize data in a plot
parks_environ.plot(column='pm25areaAvg',legend='true',
    legend_kwds={'label': "Park Area-Weighted PM 2.5 ug/m3 in 2015",
    'orientation': "horizontal"})
plt.show()

parks_environ.plot(column='no2areaAvg',legend='true',
    legend_kwds={'label': "Park Area-Weighted no2 in 2015",
    'orientation': "horizontal"})
plt.show()

# summarize environmental data by park
# can work directly on attributes and ignore geometry. e.g. take mean of polygon
# produce a new geofile to display
# can probably do this with pandas...will operate on attributes of polygons
# spatial joins

# visualize results -- not clear what exactly.
# map with park polygons color coded by environmental data measure?
# Ask Scott about visualization step
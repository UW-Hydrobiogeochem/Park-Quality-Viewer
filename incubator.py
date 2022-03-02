
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
import numpy as np

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
# water303Assess = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=1)
# water303 = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=2)
# water305 = gpd.read_file("data/WQ_ENV_WQAssessmentCurrent.gdb",driver='FileGDB',layer=3)
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
# geometry                  geometry
# water305Assess.groupby('CategoryCode').groups.keys() #'1', '2', '4A', '4B', '4C', '5'
# 1 = meets tested standards for clean water
# 2 = water of concern
# 3 = insufficient data
# 4 = impaired water that does not require a TMDL (total maximum daily loads)
# 5 = polluted water that requires a water improvement project
# water303Assess.groupby('CategoryCode').groups.keys() # 5
# water305Asses.groupby('CategoryCode').groups.keys() # '1', '2', '4A', '4B', '4C', '5'
# water305Assess.shape #(27989, 16)
# water305.shape #(27989, 16)
# water305Assess.groupby('MediumName').groups.keys() # ['Habitat', 'Other', 'Sediment', 'Tissue', 'Water']
# water305Assess.groupby('EnvironmentTypeCode').groups.keys() # ['Freshwater', 'Marine']
# NOTE: using water305Assess becuase I think this is the more recent data than water 305

# get rid of data in WQ data set that have no mappable feature. Not associated with water body
# assessmentUnitNumber says 'No Mappable Feature'
water305Assess_clean = water305Assess[water305Assess['AssessmentUnitNumber'].str.contains('No Mappable Feature')== False]
# shape: (27762, 16)
# convert codes into numbers that can operate on late in code. store in the dataframe
water305Assess_clean['CatCodeNum'] = [int(w[0]) for w in water305Assess_clean.CategoryCode]
# NOTE: gives a warning, but seems to work. So keeping it.
# water305Assess_clean_num = water305Assess_clean.copy()
# water305Assess_clean_num['CatCodeNum'] = None
# water305Assess_clean_num.loc[:,'CatCodeNum'] = [int(w[0]) for w in water305Assess_clean.CategoryCode]
# shape: (27762, 17)

# --------census data shape file
# blockgroup = gpd.read_file("data/bg10/bg10.shp")
block = gpd.read_file("data/block10/block10.shp")

# --------air quality data
# pm25 = pd.read_csv("data/CACES_PM25_2015_censusblock.csv")
pm25 = pd.read_csv("data/pm25block_wa_2015.csv")
# pm25.dtypes
no2 = pd.read_csv("data/no2block_wa_2015.csv")

# -------- parkshed polygons
parkshed_walk = gpd.read_file("data/parksheds_walk10min.geojson")
# (1435, 14)

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
parkshed_walk = parkshed_walk.to_crs(2927)
# crs conversion does not change data values. only changes geometries

#####################################################
# ---------- Align, filter, merge, clip data  ------
#####################################################
# ---------- clip data with aoi
#parks_clip = parks.clip(aoi)
parks_clip = parks # getting error when clipping, skip clip for now
water_clip = water.clip(aoi)
water305Assess_clip = water305Assess_clean.clip(aoi) 
parkshed_walk_clip = parkshed_walk.clip(aoi)

# ------- merge air quality data with census block group data to has geo reference
block_int = block.astype({'GEOID10':"int64"}) # converting data types for merge
# block_int.dtypes
block_pm25 = block_int.merge(pm25, left_on='GEOID10', right_on='block_fip')
block_no2 = block_int.merge(no2, left_on='GEOID10', right_on='block_fip')

# ---------- clip data with aoi
block_int_clip = block_int.clip(aoi)
block_pm25_clip = block_pm25.clip(aoi)
block_no2_clip = block_no2.clip(aoi)

########################################################################
# -------- intersect data layers to get environmental & pop data at each park
########################################################################

# create a new dataframe called parks_environ that holds all the enviornmental data about each park
parks_environ = parks_clip.copy()

# ---------------------------
# ------- water quality data
# ---------------------------
# create a new object that will hold buffered parks data and geometry. 
# Had to start with park geodataframe and then change geometry to be buffered geometry
# becuase when run buffer command, just get geometry out. No other data comes along.
parks_clip_buffer = parks_clip.copy() # had to use copy function in order to not affect parks_clip dataframe 
parks_clip_buffer.geometry = parks_clip.buffer(200)# in units of feet / Geoseries

# intersect buffered parks with water quality data and assign worst WQ code to the park
WQ_park_intersect = parks_clip_buffer.overlay(water305Assess_clip,how='intersection') #shape: (4203, 30)
WQ_park_intersect_max = WQ_park_intersect.groupby('OBJECTID')['CatCodeNum'].max() #len = 455
parks_environ = parks_environ.merge(WQ_park_intersect_max, how='left', left_on='OBJECTID', right_on='OBJECTID')
# TODO: might not be appropriate to assign big parks to one WQ value

# intersect buffered parks wtih water data layer from King County
water_park_intersect = parks_clip_buffer.overlay(water_clip,how='intersection')
water_park_intersect_size = water_park_intersect.groupby('OBJECTID_1')['OBJECTID_2'].size()

parks_environ = parks_environ.merge(water_park_intersect_size,how='left', left_on='OBJECTID',right_on='OBJECTID_1')

# find parks that have water but no water quality data. Assign these parks a value of 0
# parks with no water keep nan code
for i in range(len(parks_environ)):
    if np.isnan(parks_environ.loc[i,'CatCodeNum']):
        if not np.isnan(parks_environ.loc[i,'OBJECTID_2']):
            parks_environ.loc[i,'CatCodeNum']=0
# drop the column of data used to find parks with water but with no WQ data.
# because information now stored in 'CatCodeNum' column
parks_environ = parks_environ.drop(columns=['OBJECTID_2'])

#-------------------------
# ------ air quality data 
#-------------------------
# overlap parks data with air quality data
pm25_park_intersect = parks_clip.overlay(block_pm25_clip,how='intersection')
# parks_clip['OBJECTID'].is_unique # true = ID is applied to each park
# pm25_park_intersect['OBJECTID'].is_unique # false = parks have multiple air quality data
# parks_clip['SHAPE_Area'].is_unique # true
# pm25_park_intersect['SHAPE_Area'].is_unique # false...shape area is just the value of whole park carried forward
no2_park_intersect = parks_clip.overlay(block_no2_clip,how='intersection')

# ------------calculated area-averaged values for enviornmental data for each park
# example: (A1*E1 + A2*E2)/(A1+A2)

# find area of each intersection and join to the intersect object
pm25_park_intersect = pm25_park_intersect.join(pm25_park_intersect.area.to_frame(name='intersect_Area'))
no2_park_intersect = no2_park_intersect.join(no2_park_intersect.area.to_frame(name='intersect_Area'))

# multiply interesect area by air quality value for that area
pm25area = pm25_park_intersect['intersect_Area'] * pm25_park_intersect['pred15']
no2area = no2_park_intersect['intersect_Area'] * no2_park_intersect['pred15']

# join this multiplied value to the intersect object
pm25_park_intersect = pm25_park_intersect.join(pm25area.to_frame(name='pm25area'))
no2_park_intersect = no2_park_intersect.join(no2area.to_frame(name='no2area'))

# sum the multiplied values that exist within a given park and merge with parks into to a new park object
pm25_park_areasum = pm25_park_intersect.groupby('OBJECTID')['pm25area'].sum()
no2_park_areasum = no2_park_intersect.groupby('OBJECTID')['no2area'].sum()
park_tmp = parks_clip.copy()
park_tmp = park_tmp.merge(pm25_park_areasum,how='left', left_on='OBJECTID', right_on='OBJECTID')
park_tmp = park_tmp.merge(no2_park_areasum,how='left', left_on='OBJECTID', right_on='OBJECTID')

# divide sum of multiplied values by total park area to get area weighted average
pm25areaAvg = park_tmp['pm25area'].divide(park_tmp['SHAPE_Area'])
no2areaAvg = park_tmp['no2area'].divide(park_tmp['SHAPE_Area'])

# join area weighted averages to a new park object
parks_environ = parks_environ.join(pm25areaAvg.to_frame(name='pm25areaAvg'))
parks_environ = parks_environ.join(no2areaAvg.to_frame(name='no2areaAvg'))

#-----------------------
# --- Parkshed data
#---------------------
# intersect parkshed polygons with block census data
parkshed_walk_block = parkshed_walk_clip.overlay(block_int_clip,how='intersection')
# (127332, 52)
# multiple census blocks within the parkshed. Need to calculate effective population

# ------------calculated area-averaged values for population within each parkshed for each park
# example: (A1*P1 + A2*P2)/(A1+A2)

# NOTE: this calculation is not correct. Need to figure out what issue is

# find area of each intersection and join to the intersect object
parkshed_walk_block = parkshed_walk_block.join(parkshed_walk_block.area.to_frame(name='intersect_Area'))

# multiply interesect area by population race for that area
# join multiplied area to the intersect object
poplist = ['POPHISP','POPWHITE2','POPBLACK2','POPAIAN2','POPASIAN2','POPNHOPI2','POPOTH2','POPTWO2']
for pop in poplist:
    calc = parkshed_walk_block['intersect_Area'] * parkshed_walk_block[pop]
    colname = "Area_x_" + pop
    parkshed_walk_block = parkshed_walk_block.join(calc.to_frame(name=colname))
# sum multipled values with a given park and merage with parks into a temp park object
for pop in poplist:
    colname = "Area_x_" + pop
    area = parkshed_walk_block.groupby('OBJECTID')[colname].sum()
    park_tmp = park_tmp.merge(area,how='left',on='OBJECTID')
# divide sum of multiplied values by total park area to get area weighted average
# join area weighted averages to a parks_environ object
for pop in poplist:
    colname = "Area_x_" + pop
    areaavg = park_tmp[colname].divide(park_tmp['SHAPE_Area'])
    colname1 = 'Walk_' + pop
    parks_environ = parks_environ.join(areaavg.to_frame(name=colname1))

############################################
# ---------- make plots of data -----------
############################################

# ----------- make a plot of parks and water
base = parks_clip.plot(color="green")
water_clip.plot(ax=base,color="blue")
aoi.boundary.plot(ax=base,color="black")
plt.show()

# ------ plot pm25 quality data with colors showing air quality
block_pm25_clip.plot(column='pred15',legend='true',
    legend_kwds={'label': "King County PM 2.5 ug/m3 in 2015",
    'orientation': "horizontal"})
plt.show()

# ------- plot of all water quality data
base = parks_clip.plot(color="grey")
water_clip.plot(ax=base,color="black")
water305Assess_clip.plot(ax=base,column='CategoryCode',legend='true')
plt.show()

# plot water quality data assigned to parks 
base = parks_clip.plot(color='grey') 
water_clip.plot(ax=base,color='blue')
parks_environ.plot(ax=base, column='CatCodeNum',legend='true')
plt.show()

# visualize air quality data assigned to parks in a plot
parks_environ.plot(column='pm25areaAvg',legend='true',
    legend_kwds={'label': "Park Area-Weighted PM 2.5 ug/m3 in 2015",
    'orientation': "horizontal"})
plt.show()

parks_environ.plot(column='no2areaAvg',legend='true',
    legend_kwds={'label': "Park Area-Weighted no2 in 2015",
    'orientation': "horizontal"})
plt.show()

# visualize populations in walkable distance to parks
# 8 populations. 2x4 subplot
plt.figure(figsize=(15, 20))
plt.subplots_adjust(hspace=0.5)
loopnum = 0
for pop in poplist:
    loopnum = loopnum +1
    colname = "Walk_" + pop
    ax = plt.subplot(4,2,loopnum)
    parks_environ.plot(ax=ax,column=colname,legend='true',legend_kwds={'label': 
    colname, 'orientation': "horizontal"})
plt.show()
# plotting does not seem correct.


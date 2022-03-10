
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

parks_environ.rename(columns = {'CatCodeNum':'WQ Category','pm25areaAvg':'PM 2.5 (ug/m^3)','no2areaAvg':'NO2 (ppb)'
    ,'walk_totalPop':'Total Walkable Pop','walk_pct_NotWhite':'Frac Non-White Walkable Pop'},inplace=True)

# Create a map
config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': 'weyfwj8',
     'type': 'geojson',
     'config': {'dataId': 'Park Quality',
      'label': 'Water Quality',
      'color': [77, 193, 156],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'geojson': 'geometry'},
      'isVisible': True,
      'visConfig': {'opacity': 1,
       'strokeOpacity': 0.8,
       'thickness': 0.2,
       'strokeColor': [25, 20, 16],
       'colorRange': {'name': 'ColorBrewer YlOrRd-6',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#ffffb2',
         '#fed976',
         '#feb24c',
         '#fd8d3c',
         '#f03b20',
         '#bd0026']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#E5E0E1']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': True,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'WQ Category',
       'type': 'string'},
      'colorScale': 'ordinal',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}},
    {'id': '6chpvdn',
     'type': 'geojson',
     'config': {'dataId': 'Park Quality',
      'label': 'Air Quality (PM 2.5)',
      'color': [179, 173, 158],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'geojson': 'geometry'},
      'isVisible': False,
      'visConfig': {'opacity': 1,
       'strokeOpacity': 0.8,
       'thickness': 0.2,
       'strokeColor': [25, 20, 16],
       'colorRange': {'name': 'ColorBrewer PuRd-6',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#f1eef6',
         '#d4b9da',
         '#c994c7',
         '#df65b0',
         '#dd1c77',
         '#980043']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': True,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'PM 2.5 (ug/m^3)',
       'type': 'real'},
      'colorScale': 'quantize',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}},
    {'id': 'dfl0yn',
     'type': 'geojson',
     'config': {'dataId': 'Park Quality',
      'label': 'Air Quality (NO2)',
      'color': [18, 147, 154],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'geojson': 'geometry'},
      'isVisible': False,
      'visConfig': {'opacity': 1,
       'strokeOpacity': 0.8,
       'thickness': 0.2,
       'strokeColor': [25, 20, 16],
       'colorRange': {'name': 'ColorBrewer PuRd-6',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#f1eef6',
         '#d4b9da',
         '#c994c7',
         '#df65b0',
         '#dd1c77',
         '#980043']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': True,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'NO2 (ppb)', 'type': 'real'},
      'colorScale': 'quantize',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}},
    {'id': 'gayqlek',
     'type': 'geojson',
     'config': {'dataId': 'Park Quality',
      'label': 'Walkability (Population)',
      'color': [30, 150, 190],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'geojson': 'geometry'},
      'isVisible': False,
      'visConfig': {'opacity': 1,
       'strokeOpacity': 0.8,
       'thickness': 0.2,
       'strokeColor': [25, 20, 16],
       'colorRange': {'name': 'ColorBrewer YlGnBu-6',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#ffffcc',
         '#c7e9b4',
         '#7fcdbb',
         '#41b6c4',
         '#2c7fb8',
         '#253494']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': True,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'Total Walkable Pop',
       'type': 'real'},
      'colorScale': 'quantile',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}},
    {'id': '6khzc68',
     'type': 'geojson',
     'config': {'dataId': 'Park Quality',
      'label': 'Walkability (Race)',
      'color': [18, 92, 119],
      'highlightColor': [252, 242, 26, 255],
      'columns': {'geojson': 'geometry'},
      'isVisible': False,
      'visConfig': {'opacity': 1,
       'strokeOpacity': 0.8,
       'thickness': 0.2,
       'strokeColor': [25, 20, 16],
       'colorRange': {'name': 'ColorBrewer YlGn-6',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#ffffcc',
         '#d9f0a3',
         '#addd8e',
         '#78c679',
         '#31a354',
         '#006837']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': True,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'Frac Non-White Walkable Pop',
       'type': 'real'},
      'colorScale': 'quantize',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'Park Quality': [{'name': 'KC_FAC_FID',
        'format': None},
       {'name': 'KCPARKFID', 'format': None},
       {'name': 'SITENAME', 'format': None},
       {'name': 'SITETYPE', 'format': None}]},
     'compareMode': False,
     'compareType': 'absolute',
     'enabled': True},
    'brush': {'size': 0.5, 'enabled': False},
    'geocoder': {'enabled': False},
    'coordinate': {'enabled': False}},
   'layerBlending': 'normal',
   'splitMaps': [],
   'animationConfig': {'currentTime': None, 'speed': 1}},
  'mapState': {'bearing': 0,
   'dragRotate': False,
   'latitude': 47.4985995190805,
   'longitude': -122.09381251187126,
   'pitch': 0,
   'zoom': 8.991986749720091,
   'isSplit': False},
  'mapStyle': {'styleType': 'light',
   'topLayerGroups': {},
   'visibleLayerGroups': {'label': True,
    'road': False,
    'border': False,
    'building': True,
    'water': True,
    'land': True,
    '3d building': False},
   'threeDBuildingColor': [218.82023004728686,
    223.47597962276103,
    223.47597962276103],
   'mapStyles': {}}}}

map=KeplerGl(height=600, data={'Park Quality': parks_environ}, config=config)
map.save_to_html(data={'Park Quality': parks_environ}, config=config, file_name="outputs/kingco_parks.html")




##############################################
# ------------- Scatter Plots ---------------
##############################################

# # compare park demographic data against park environmental quality data
# fig1 = px.scatter(parks_environ,x='walk_totalPop',y='pm25areaAvg',color='walk_pct_NotWhite', hover_data=['SITENAME'])
# fig1.show()
# fig2 = px.scatter(parks_environ,x='walk_totalPop',y='no2areaAvg',color='walk_pct_NotWhite', hover_data=['SITENAME'])
# fig2.show()

# # water quality
# parks_environ_plot = parks_environ[pd.notna(parks_environ['CatCodeNum'])]
# fig = px.scatter(parks_environ_plot,x='walk_totalPop',y='walk_pct_NotWhite' ,color='CatCodeNum', 
#     hover_data=['SITENAME'],color_continuous_scale=px.colors.sequential.Sunsetdark)
# fig.show()
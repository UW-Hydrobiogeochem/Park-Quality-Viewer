# Park Quality Viewer: Environmental Quality of and Population Served by Public Green and Blue Spaces

## Project Objective
The overarching goal of this project is to compile information about the environmental quality of public green and blue spaces along with demographic information about potential users of those spaces to enhance understanding of the benefits and risks associated with accessing these spaces and to identify public spaces where efforts to improve environmental quality would have a potentially large, positive impact.

## Approach
King County in Washington State was used as the focal area for development of the code and approach. Considered environmental data included water quality and air quality. Population served was based on 10-minute walk and 10-minute drive.

## Data Sources
* Water quality 
    * based on federally mandated water quality assessment based on the Clean Water Act.    
    * Downloaded from [State of Washington](https://geo.wa.gov/maps/waecy::waecy-water-quality-assessment-303d-list-current/about)
* Air quality
    * related to data available from the [Center for Air, Climate, & Energy Solutions](https://www.caces.us/)
    * CACES data are publicly available at the Census Block Group level. 
    * Code uses non-publicly available data at the Block level. 
    * Contact owner of this repository if you are interested in accessing these data
* Parks
    * Park data from [King County GIS Open Data portal](https://gis-kingcounty.opendata.arcgis.com/datasets/parks-in-king-county-park-area/explore?location=47.461100%2C-121.802650%2C10.45)
* Water
    * Water data from [King County GIS Open Data portal](https://gis-kingcounty.opendata.arcgis.com/datasets/open-water-for-king-county-and-portions-of-adjacent-counties-wtrbdy-area/explore?location=47.659250%2C-123.032200%2C8.28)
* Area of Interest
    * [King County GIS Open Data portal](https://gis-kingcounty.opendata.arcgis.com/datasets/king-county-political-boundary-no-waterbodies-kingco-area/explore?location=47.431150%2C-121.809650%2C10.30)
* Census Block (2010)
    * [Census.gov](http://www.census.gov/geo/www/tiger)
* Walking and Driving Areas for parks
    * forthcoming independent repository
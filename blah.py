import arcpy

# Set the project file path
project_path = r"C:\\Users\\Geo-Tech\\Desktop\\blah\\testproject.aprx"
layout_name = "Layout"
mapFrameName = "Map Frame"
mapName = "Map"
longitude = -113.235
latitude = 53.052
new_scale = 5000
spatial_ref = arcpy.SpatialReference(4326) # WGS 1984
width = 100
height = 100
x_loc = 0.45
y_loc = 0.00

aprx = arcpy.mp.ArcGISProject(project_path)
layoutList = aprx.listLayouts(layout_name)[0]


def updateTextElement(layoutList,oldTextElement, newTextElement):
    text_elements = layoutList.listElements("TEXT_ELEMENT")
    for text_element in text_elements:
        if text_element.name == oldTextElement:
        
            text_element.text = newTextElement
            print(text_element.name)
            print(text_element.text)


def setCenterGrid(aprx, longitude, latitude, spatial_ref, mapFrameName):
    # Access map and map frame
    map = aprx.listMaps(mapName)[0]
    layout = aprx.listLayouts(layout_name)[0]
    map_frame = layout.listElements("MAPFRAME_ELEMENT", mapFrameName)[0]

    # Get the spatial reference of the map
    map_spatial_ref = map.spatialReference
    mf = map_frame
    # Create a point geometry and project it to the spatial reference of the map
    point = arcpy.Point(longitude, latitude)
    point_geometry = arcpy.Geometry('Point', point, spatial_ref)
    projected_geometry = point_geometry.projectAs(map_spatial_ref)

    # Set the center of the extent to the projected point geometry
    extent_x = projected_geometry.extent.XMin + (projected_geometry.extent.XMax - projected_geometry.extent.XMin) / 2
    extent_y = projected_geometry.extent.YMin + (projected_geometry.extent.YMax - projected_geometry.extent.YMin) / 2
    new_extent = arcpy.Extent(extent_x - 1000, extent_y - 1000, extent_x + 1000, extent_y + 1000)
    map_frame.camera.setExtent(new_extent)


# Set the scale of the map frame
def setScale(new_scale):
    map = aprx.listMaps(mapName)[0]
    layout = aprx.listLayouts(layout_name)[0]
    map_frame = layout.listElements("MAPFRAME_ELEMENT", mapFrameName)[0]
    mf = map_frame
    mf.camera.scale = new_scale


def mainLoop():
    updateTextElement(layoutList,"Title","blahblah3")
    setCenterGrid(aprx,longitude, latitude,spatial_ref, mapFrameName)
    setScale(new_scale)
    aprx.save()

mainLoop()

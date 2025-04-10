import arcpy
import time

# ArcGIS input parameters
Boundary = arcpy.GetParameterAsText(0)
cell_size = arcpy.GetParameterAsText(1)
SHP_path = arcpy.GetParameterAsText(2)
raster_path = arcpy.GetParameterAsText(3)
archive_path = arcpy.GetParameterAsText(4)

# Create a timer function
def TellTime(t0, tf):
    if tf - t0 < 60:
        arcpy.AddMessage('Run Time = {} seconds.'.format(round(tf-t0,3)))
    else:
        arcpy.AddMessage('Run Time = {} minutes.'.format(round((tf-t0)/60,3)))


# Get the min and max X and Y of the FLO-2D boundary
t0 = time.time()
arcpy.AddMessage('\nObtaining coordinates of boundary shapefile.')
desc = arcpy.Describe(Boundary)
Xmin = desc.Extent.XMin
Xmax = desc.Extent.XMax
Ymin = desc.Extent.YMin
Ymax = desc.Extent.YMax

# Create set of coordinates needed to create fishnet shapefile
Origin = '{} {}'.format(Xmin, Ymin)
Yaxis = '{} {}'.format(Xmin, Ymax)
UpperRight = '{} {}'.format(Xmax, Ymax)
tf = time.time()
TellTime(t0, tf)

# Create fishnet shapefile
t0 = time.time()
arcpy.AddMessage('\nCreating intermediate fishnet shapefile.')
fishnet = archive_path + r'\fishnet.shp'
fishnetPnts = archive_path + r'\fishnet_label.shp'
arcpy.CreateFishnet_management(fishnet, Origin, Yaxis, cell_size, cell_size, 0, 0, UpperRight, 'LABELS', Boundary, "POLYGON")
arcpy.MakeFeatureLayer_management(fishnet, 'fishnet_lyr')
arcpy.MakeFeatureLayer_management(fishnetPnts, 'fishnetPnts_lyr')
tf = time.time()
TellTime(t0, tf)

# Select grid by location and export to new shapefile.
t0 = time.time()
arcpy.AddMessage('\nCreating grid shapefile.')
GRID = SHP_path + r'\GRID.shp'
arcpy.SelectLayerByLocation_management('fishnet_lyr', 'HAVE_THEIR_CENTER_IN',  Boundary)
arcpy.FeatureClassToFeatureClass_conversion('fishnet_lyr', SHP_path, 'GRID')
tf = time.time()
TellTime(t0, tf)

# Select centroids by location and export to new shapefile.
t0 = time.time()
arcpy.AddMessage('\nCreating grid points shapefile.')
GRID_PNTS = SHP_path + r'\GRID_PNTS.shp'
arcpy.SelectLayerByLocation_management('fishnetPnts_lyr', 'HAVE_THEIR_CENTER_IN',  Boundary)
arcpy.FeatureClassToFeatureClass_conversion('fishnetPnts_lyr', SHP_path, 'GRID_PNTS')
tf = time.time()
TellTime(t0, tf)
    
# Add fields to the grid centroids shapefile attribute table
t0 = time.time()
arcpy.AddMessage('\nAdding fields to grid points attribute table (FLO2D_ID, centroid).')
arcpy.AddGeometryAttributes_management(GRID_PNTS, 'POINT_X_Y_Z_M')
arcpy.AddGeometryAttributes_management(GRID, 'CENTROID')
arcpy.AddField_management(GRID_PNTS, 'FLO2D_ID', 'LONG', '10')
arcpy.AddField_management(GRID, 'FLO2D_ID', 'LONG', '','','10')
tf = time.time()
TellTime(t0, tf)

# Add FLO-2D grid element ID's
t0 = time.time()
arcpy.AddMessage("\nAdding grid cell ID's.")
with arcpy.da.UpdateCursor(GRID_PNTS, ['FLO2D_ID']) as cursor:
    FLO2D_ID = 1
    for row in cursor:
        row[0] = FLO2D_ID
        cursor.updateRow(row)
        FLO2D_ID += 1

with arcpy.da.UpdateCursor(GRID, 'FLO2D_ID') as cursor:
    FLO2D_ID = 1
    for row in cursor:
        row[0] = FLO2D_ID
        cursor.updateRow(row)
        FLO2D_ID += 1

# Create GRID raster
arcpy.AddMessage('\nCreating FLO-2D Grid raster.')
gridRaster = raster_path + r'\gridRaster'
arcpy.FeatureToRaster_conversion(GRID, 'FLO2D_ID', gridRaster, cell_size)
arcpy.env.snapRaster = gridRaster

tf = time.time()
TellTime(t0, tf)

arcpy.AddMessage('\nDONE!')      
        
        

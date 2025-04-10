import arcpy

REF_Grids = arcpy.GetParameterAsText(0)
GRID_PNTS = arcpy.GetParameterAsText(1)
Elevation = arcpy.GetParameterAsText(2)
ELEV_Field_Name = arcpy.GetParameterAsText(3)
ELEV_TYPE = arcpy.GetParameterAsText(4)
raster_path = arcpy.GetParameterAsText(5)

# Create a timer function
def TellTime(t0, tf):
    if tf - t0 < 60:
        arcpy.AddMessage('Run Time = {} seconds.'.format(round(tf-t0,3)))
    else:
        arcpy.AddMessage('Run Time = {} minutes.'.format(round((tf-t0)/60,3)))

# Obtain coordinate system of GRID shapefile
Coor_System = arcpy.Describe(GRID_PNTS).spatialReference
arcpy.overwriteOutput = True

if ELEV_TYPE == 'MAX':
    t0 = time.time()
    # Create max and min elevation rasters
    elev_max = arcpy.sa.CellStatistics(Elevation, 'MAXIMUM', 'DATA')
    elev_max.save(raster_path + r'\elev_max.img')

    arcpy.AddMessage('\nUpdating grid points shapefile with maximum elevations.')
    arcpy.SelectLayerByLocation_management(GRID_PNTS, 'HAVE_THEIR_CENTER_IN', REF_Grids)
    arcpy.AddSurfaceInformation_3d(GRID_PNTS, elev_max, 'Z')
    with arcpy.da.UpdateCursor(GRID_PNTS, ['ELEV', 'ELEV_TYPE', 'Z']) as cursor:
        for row in cursor:
            if row[2] > 0:
                row[0] = row[2]
                row[1] = ELEV_TYPE
                cursor.updateRow(row)

    arcpy.DeleteField_management(GRID_PNTS, 'Z')
    tf = time.time()
    TellTime(t0, tf)

    arcpy.SelectLayerByAttribute_management(GRID_PNTS, 'CLEAR_SELECTION')
    arcpy.AddMessage('\nDONE!')

elif ELEV_TYPE == 'MIN':
    # Create max and min elevation rasters
    elev_min = arcpy.sa.CellStatistics(Elevation, 'MINIMUM', 'DATA')
    elev_min.save(raster_path + r'\elev_min.img')

    arcpy.AddMessage('\nUpdating grid points shapefile with minimum elevations.')
    arcpy.SelectLayerByLocation_management(GRID_PNTS, 'HAVE_THEIR_CENTER_IN', REF_Grids)
    arcpy.AddSurfaceInformation_3d(GRID_PNTS, elev_min, 'Z')
    with arcpy.da.UpdateCursor(GRID_PNTS, ['ELEV', 'ELEV_TYPE', 'Z']) as cursor:
        for row in cursor:
            if row[2] > 0:
                row[0] = row[2]
                row[1] = ELEV_TYPE
                cursor.updateRow(row)

    arcpy.DeleteField_management(GRID_PNTS, 'Z')
    tf = time.time()
    TellTime(t0, tf)
    arcpy.SelectLayerByAttribute_management(GRID_PNTS, 'CLEAR_SELECTION')
    
    arcpy.AddMessage('\nDONE!')


elif ELEV_TYPE == 'SET':
    new_grid_data = []
    with arcpy.da.SearchCursor(REF_Grids, ['FLO2D_ID', ELEV_Field_Name]) as cursor:
        for row in cursor:
            new_data = (row[0], row[1], ELEV_TYPE)
            new_grid_data.append(new_data)
           
    arcpy.SelectLayerByLocation_management(GRID_PNTS, 'HAVE_THEIR_CENTER_IN', REF_Grids)

    for data in new_grid_data:
        with arcpy.da.UpdateCursor(GRID_PNTS, ['FLO2D_ID', 'ELEVATION', 'ELEV_TYPE']) as cursor:
            for row in cursor:
                if data[0] == row[0]:
                    row[1] = data[1]
                    row[2] = data[2]
                    cursor.updateRow(row)

elif ELEV_TYPE == '+/-':
    cell_size=20
    Grid_Ref_raster = raster_path + r'\ref_addsub'
    arcpy.FeatureToRaster_conversion(REF_Grids, ELEV_Field_Name, Grid_Ref_raster, cell_size)

    # Get elevation change data from raster at centroid points
    arcpy.AddMessage("\nExtracting elevation change from raster for each cell.")
    t0 = time.time()
    arcpy.SelectLayerByLocation_management(GRID_PNTS, 'HAVE_THEIR_CENTER_IN',  REF_Grids, '', 'NEW_SELECTION')
    arcpy.AddSurfaceInformation_3d(GRID_PNTS, Grid_Ref_raster, 'Z')
    arcpy.CalculateField_management(GRID_PNTS, 'ELEV', '[ELEV]+[Z]', 'VB', '')
    arcpy.CalculateField_management(GRID_PNTS, 'ELEV_TYPE', '+/-', 'PYTHON', '')
    arcpy.DeleteField_management(GRID_PNTS, 'Z')
    tf = time.time()
    TellTime(t0, tf)

    

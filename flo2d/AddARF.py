grid_pnts = arcpy.GetParameterAsText(0)
grid = arcpy.GetParameterAsText(1)
gridIDField = arcpy.GetParameterAsText(2)
arf = arcpy.GetParameterAsText(3)
outPath = arcpy.GetParameterAsText(4)

# Create shapefile for intersection of grid and ARF features
gridARF_intersect = outPath + r'\GridArf_Intersect.shp'
arcpy.Intersect_analysis([arf, grid], gridARF_intersect, "ALL", "", "INPUT")

# Create dictionary of grid ID and intersection area
result = arcpy.GetCount_management(gridARF_intersect)
intersect_count = int(result[0])
# Initialize dictionary
intersect_Dict = {i+1: 0 for i in range(intersect_count)}
# Add intersection areas to dicitionary by grid ID
with arcpy.da.SearchCursor(gridARF_intersect, [gridIDField, 'SHAPE@AREA']) as cursor:
    for row in cursor:
        intersect_Dict[row[0]] = row[1]
        
# Get area of grid
    with arcpy.da.SearchCursor(grid, ['SHAPE@AREA']) as cursor:
        for row in cursor:
            gridArea = row[0]
            break
# Add ARF field to grid points shapefile
arcpy.AddField_management(grid_pnts, 'ARF', 'FLOAT', 3, 2)  
      
# Calculate ARF for each grid and append to GRID_PNTS.shp attribute table
with arcpy.da.UpdateCursor(grid_pnts, [gridIDField, 'ARF']) as cursor:
    for row in cursor:
        if row[0] in intersect_Dict.keys():
            arf_value = intersect_Dict[row[0]]/gridArea
            if arf_value > 0.89:
                arf_value = 1
                
            row[1] = arf_value

        cursor.updateRow(row)


    

elevRefinement = arcpy.GetParameterAsText(0)
grid = arcpy.GetParameterAsText(1)
elev_matchField = arcpy.GetParameterAsText(2)
grid_matchField = arcpy.GetParameterAsText(3)
elev_elevationField = arcpy.GetParameterAsText(4)
grid_elevationField = arcpy.GetParameterAsText(5)

elevDict = {}

with arcpy.da.SearchCursor(elevRefinement, [elev_matchField, elev_elevationField]) as cursor:
    for row in cursor:
        elevDict[row[0]] = row[1]

with arcpy.da.UpdateCursor(grid, [grid_matchField, grid_elevationField]) as cursor:
    for row in cursor:
        if row[0] in elevDict.keys():
            row[1] = elevDict[row[0]]
            cursor.updateRow(row)


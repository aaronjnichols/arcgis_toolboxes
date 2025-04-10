import arcpy

strc_lines = arcpy.GetParameterAsText(0)
grid_raster = arcpy.GetParameterAsText(1)

# Add inflow/outflow node fields
arcpy.AddField_management(strc_lines, 'INFLONOD', 'TEXT')
arcpy.AddField_management(strc_lines, 'OUTFLONOD', 'TEXT')

# Determine inflow/outflow ID's from grid raster
with arcpy.da.SearchCursor(strc_lines, ["OID@", "SHAPE@"]) as cursor:
    inflows = []
    outflows = []
    for row in cursor:
        strt_X = str(row[1].firstPoint.X)
        strt_Y = str(row[1].firstPoint.Y)
        end_X = str(row[1].lastPoint.X)
        end_Y = str(row[1].lastPoint.Y)

        # Concatenate x, y coordinates for GetCellValue tool formatting
        strtCoord = strt_X + ' ' + strt_Y
        endCoord = end_X + ' ' + end_Y
        strtCell_result = arcpy.GetCellValue_management(grid_raster, strtCoord)
        endCell_result = arcpy.GetCellValue_management(grid_raster, endCoord)
        inflows.append(strtCell_result.getOutput(0))
        outflows.append(endCell_result.getOutput(0))

# Fill attribute table with inflow/outflow IDs
i = 0
with arcpy.da.UpdateCursor(strc_lines, ['INFLONOD', 'OUTFLONOD']) as cursor:
    for row in cursor:
        row[0] = inflows[i]
        row[1] = outflows[i]
        cursor.updateRow(row)
        i+=1







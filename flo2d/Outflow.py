outflow_lines = arcpy.GetParameterAsText(0)
case_field = arcpy.GetParameterAsText(1)
outflow_location_field = arcpy.GetParameterAsText(2)
grid = arcpy.GetParameterAsText(3)
id_field = arcpy.GetParameterAsText(4)
outpath = arcpy.GetParameterAsText(5)

# Create OUTFLOW.DAT file to write to
OUTFLOW = open(r'{}\OUTFLOW.DAT'.format(outpath), 'w')

# Select each outflow line one at a time and select grids that intersect the line
with arcpy.da.SearchCursor(outflow_lines, [case_field, outflow_location_field]) as cur:
    for row in cur:
	line_id = row[0]
        out_num = int(row[1])
        arcpy.SelectLayerByAttribute_management(outflow_lines, 'NEW_SELECTION', '''"{}" = {}'''.format(case_field, line_id))
        arcpy.SelectLayerByLocation_management(grid, 'INTERSECT', outflow_lines, '', 'NEW_SELECTION')

        # Get grid ids and write to OUTFLOW.DAT
        with arcpy.da.SearchCursor(grid, id_field) as cur2:
            for count, row2 in enumerate(cur2):
                grid_id = int(row2[0])
                if out_num > 0:
                    OUTFLOW.write('%-6s %-s\n' % ('O{}'.format(out_num), grid_id))
                else:
                    OUTFLOW.write('%-6s %-s\n' % ('O', grid_id))

        arcpy.AddMessage('{} outflow cells for location {}'.format(count, out_num))

OUTFLOW.close()
                 

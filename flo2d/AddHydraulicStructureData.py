import arcpy
import math

# Inputs
strc_lines = arcpy.GetParameterAsText(0)
strucName = arcpy.GetParameterAsText(1)
numPipes = arcpy.GetParameterAsText(2)
diameter = arcpy.GetParameterAsText(3)
width = arcpy.GetParameterAsText(4)
height = arcpy.GetParameterAsText(5)
grid_raster = arcpy.GetParameterAsText(6)

# Calculate FLO2D input parameters. Convert multiple pipes to equivalent box
fields = [strucName, numPipes, diameter, width, height]
with arcpy.da.SearchCursor(strc_lines, fields) as cursor:
    strcDict = {}
    for row in cursor:
        STRUCTNAME = row[0]
        if row[1] == 1 and row[2] > 0:
            TYPEC = 2
            Area = math.pi * (row[2]**2)/4 * row[1]
            CUBASE = 0
            CDIAMETER = row[2]

        elif row[1] > 1 and row[2] > 0:
            TYPEC = 1
            Area = math.pi * (row[2]**2)/4 * row[1]
	    CDIAMETER = row[2]
            CUBASE = Area/CDIAMETER
            

        elif row[2] == 0:
            TYPEC = 1
            Area = row[1] * row[3] * row[4]
            CDIAMETER = row[4]
	    CUBASE = Area/CDIAMETER
        else:
            TYPEC = 9999
            Area = 9999
            CUBASE = 9999
            CDIAMETER = 9999

        strcDict[STRUCTNAME] = [TYPEC, Area, CUBASE, CDIAMETER]

# Add calculated data to attribute table
with arcpy.da.UpdateCursor(strc_lines, ['STRUCTNAME', 'TYPEC', 'Area', 'CUBASE', 'CDIAMETER']) as cursor:
    for row in cursor:
        strc = strcDict[row[0]]
        row[1] = strc[0]
        row[2] = strc[1]
        row[3] = strc[2]
        row[4] = strc[3]
        cursor.updateRow(row)

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
        


import arcpy
import time

# Inputs
gridPnts = arcpy.GetParameterAsText(0)
gridIDField = arcpy.GetParameterAsText(1)
outPath = arcpy.GetParameterAsText(2)

# Create blank .dat files to write GIS data to.
cadpts = open(outPath+r'\CADPTS.DAT', 'w')

# Loop through Grid Points shapefile and write data to .dat files 
with arcpy.da.SearchCursor(gridPnts, [gridIDField, 'SHAPE@X', 'SHAPE@Y']) as cursor:
    for row in cursor:
        ID = int(row[0])
        x = round(float(row[1]),0)
        y = round(float(row[2]),0)
        cadpts.write('%-12s %-15s %s\n' % (ID, x, y))

cadpts.close()
arcpy.AddMessage('DONE!')
                           

        
        
        

import arcpy
import time
from math import log10, exp, log

# Inputs
soils = arcpy.GetParameterAsText(0)
xksatField = arcpy.GetParameterAsText(1)
rtimpnField = arcpy.GetParameterAsText(2)
sdepthField = arcpy.GetParameterAsText(3)
landUse = arcpy.GetParameterAsText(4)
saturationField = arcpy.GetParameterAsText(5)
gridPnts = arcpy.GetParameterAsText(6)
grid = arcpy.GetParameterAsText(7)
gridIDField = arcpy.GetParameterAsText(8)
outPath = arcpy.GetParameterAsText(9)

# Create a timer function
def TellTime(t0, tf):
    if tf - t0 < 60:
        arcpy.AddMessage('Run Time = {} seconds.'.format(round(tf-t0,3)))
    else:
        arcpy.AddMessage('Run Time = {} minutes.'.format(round((tf-t0)/60,3)))

# Create union of soils and surface feature shapefiles
arcpy.AddMessage('\nCreating union of soils and land use shapefiles. Determining DTHETA based on land use saturation condition.')
t0 = time.time()
Soils_LU_Union = outPath + r'/Soils_LU_Union.shp'
arcpy.Union_analysis([soils, landUse], Soils_LU_Union)
tf = time.time()
TellTime(t0, tf)

arcpy.AddField_management(Soils_LU_Union, 'DTHETA', 'FLOAT', 5, 4)
arcpy.AddField_management(Soils_LU_Union, 'PSIF', 'FLOAT', 7, 4)

# Calculate PSIF and DTHETA from XKSAT and initial saturation
with arcpy.da.UpdateCursor(Soils_LU_Union, [xksatField, saturationField, 'DTHETA', 'PSIF']) as cursor:
    for row in cursor:
        saturation = row[1].lower()[0]
        xksat = row[0]
        psif = exp(0.9813 - 0.439 * log(xksat) + 0.0051 * (log(xksat))**2 + 0.0060 * (log(xksat))**3)
    
        if saturation == 'd':
            if 0.01 <= xksat <= 0.15:
                dtheta = exp(-0.2394 + 0.3616 * log(xksat))
            elif 0.15 < xksat <= 0.25:
                dtheta = exp(-1.4122 - 0.2614 * log(xksat))
            elif 0.25 < xksat:
                dtheta = 0.35
        elif saturation == 'n':
            if 0.01 <= xksat <= 0.02:
                dtheta = exp(1.6094 + log(xksat))
            elif 0.02 < xksat <= 0.04:
                dtheta = exp(-0.0142 + 0.585 * log(xksat))
            elif 0.04 < xksat <= 0.1:
                dtheta = 0.15
            elif 0.1 < xksat <= 0.15:
                dtheta = exp(1.0038 + 1.2599 * log(xksat))
            elif 0.15 < xksat <= 0.4:
                    dtheta = 0.25
            elif 0.4 < xksat:
                    dtheta = exp(-1.2342 + 0.1660 * log(xksat))
        elif saturation == 's':
            dtheta = 0.0
        else:
            dtheta = 9999

        row[2] = dtheta
        row[3] = psif
        cursor.updateRow(row)

# Create intersection of soils/surface features with the grid
arcpy.AddMessage('\nCreating intersection of soils/land use with grid.')
t0 = time.time()
soilsLandUse_grid = outPath + r'/SoilsLandUse_grid.shp'
arcpy.Intersect_analysis([Soils_LU_Union, grid], soilsLandUse_grid)
result = arcpy.GetCount_management(soilsLandUse_grid)
intersect_count = int(result[0])
tf = time.time()
TellTime(t0, tf)

# Calculate grid area
with arcpy.da.SearchCursor(grid, ['SHAPE@AREA']) as cursor:
    for row in cursor:
        gridArea = row[0]
        break
    
# Fill dictionary with grid ID's and calculate average RTIMPN and Soil Depth           
with arcpy.da.SearchCursor(soilsLandUse_grid, [gridIDField, rtimpnField, sdepthField, xksatField, 'DTHETA', 'PSIF', 'SHAPE@AREA']) as cursor:
    rtimpnDict = {i+1: [] for i in range(intersect_count)}
    sdepthDict = {i+1: [] for i in range(intersect_count)}
    xksatDict = {i+1: [] for i in range(intersect_count)}
    dthetaDict = {i+1: [] for i in range(intersect_count)}
    psifDict = {i+1: [] for i in range(intersect_count)}
    for row in cursor:
        rtimpnDict[row[0]].append(row[1]*row[6]/gridArea)
        sdepthDict[row[0]].append(row[2]*row[6]/gridArea)
        xksatDict[row[0]].append(log10(row[3])*row[6]/gridArea)
        dthetaDict[row[0]].append(row[4]*row[6]/gridArea)
        psifDict[row[0]].append(row[5]*row[6]/gridArea)
    
# Add XKSAT, DTHETA, PSIF, RTIMPN, RTIMP and SDEPTH to gridPnts attribute table
arcpy.AddField_management(gridPnts, 'XKSAT', 'FLOAT', 5, 4)
arcpy.AddField_management(gridPnts, 'DTHETA', 'FLOAT', 5, 4)
arcpy.AddField_management(gridPnts, 'PSIF', 'FLOAT', 7, 4)
arcpy.AddField_management(gridPnts, 'RTIMPN', 'FLOAT', 5, 4)
arcpy.AddField_management(gridPnts, 'RTIMP', 'FLOAT', 5, 4)
arcpy.AddField_management(gridPnts, 'SDEPTH', 'FLOAT', 6, 4)

# Loop through dictionaries and add data to the grid points attribute table. Calculate RTIMP.
with arcpy.da.UpdateCursor(gridPnts, [gridIDField, 'XKSAT', 'DTHETA', 'PSIF', 'RTIMPN', 'SDEPTH', 'RTIMPL', 'RTIMP']) as cursor:
    for row in cursor:
        row[1] = 10**sum(xksatDict[row[0]])
        row[2] = sum(dthetaDict[row[0]])
        row[3] = sum(psifDict[row[0]])
        rtimpn = sum(rtimpnDict[row[0]])
        row[4] = rtimpn
        row[5] = sum(sdepthDict[row[0]])
        rtimp = rtimpn  + row[6]
        if rtimp > 1:
            rtimp = 1
        row[7] = rtimp
        cursor.updateRow(row)
    

import arcpy
import os

soils = arcpy.GetParameterAsText(0)
soil_id = arcpy.GetParameterAsText(1)
wpoint = arcpy.GetParameterAsText(2)
fcapac = arcpy.GetParameterAsText(3)
sat = arcpy.GetParameterAsText(4)
rtimpn = arcpy.GetParameterAsText(5)
landuse = arcpy.GetParameterAsText(6)
landuse_id = arcpy.GetParameterAsText(7)
rtimpl = arcpy.GetParameterAsText(8)
sat_cond = arcpy.GetParameterAsText(9)
outpath = arcpy.GetParameterAsText(10)

# create union of soils and land use
if '.gdb' in outpath:
    soils_landuse = os.path.join(outpath, 'Soils_LandUse_UNION')
else:
    soils_landuse = os.path.join(outpath, 'Soils_LandUse_UNION.shp')
arcpy.Union_analysis([soils, landuse], soils_landuse)

# calculate dtheta values
arcpy.AddField_management(soils_landuse, "DTHETAdry", "FLOAT", 3, 2)
arcpy.AddField_management(soils_landuse, "DTHETAnorm", "FLOAT", 3, 2)

arcpy.CalculateField_management(soils_landuse, "DTHETAdry", '!{}! - !{}!'.format(sat, wpoint), "PYTHON")
arcpy.CalculateField_management(soils_landuse, "DTHETAnorm", '!{}! - !{}!'.format(sat, fcapac), "PYTHON")

# determine dtheta value to be used based on saturated condition
arcpy.AddField_management(soils_landuse, "DTHETA", "FLOAT", 3, 2)

with arcpy.da.UpdateCursor(soils_landuse, [sat_cond, "DTHETAdry", "DTHETAnorm", "DTHETA"]) as cur:
    for row in cur:
        if len(row[0]) > 0:
		if row[0].lower()[0] == 'd':
            		row[3] = row[1]
        	elif row[0].lower()[0] == 'n':
            		row[3] = row[2]
        	elif row[0].lower()[0] == 's':
            		row[3] = 0
        	else:
            		row[3] = -9.99
	else:
		row[3] = -9.99
        cur.updateRow(row)

# determine initial water content value to be used based on saturated condition
arcpy.AddField_management(soils_landuse, "IniWatCont", "FLOAT", 3, 2)

with arcpy.da.UpdateCursor(soils_landuse, [sat_cond, sat, wpoint, fcapac, "IniWatCont"]) as cur:
    for row in cur:
        if len(row[0]) > 0:
		if row[0].lower()[0] == 'd':
            		row[4] = row[2]
        	elif row[0].lower()[0] == 'n':
            		row[4] = row[3]
        	elif row[0].lower()[0] == 's':
            		row[4] = row[1]
        	else:
            		row[4] = -9.99
	else:
		row[4] = -9.99
        cur.updateRow(row)
        
# Calculate total percent imperviousness
arcpy.AddField_management(soils_landuse, "RTIMPtotal", "SHORT", 3)

with arcpy.da.UpdateCursor(soils_landuse, [rtimpl, rtimpn, "RTIMPtotal"]) as cur:
    for row in cur:
        rtimp_calc = row[0] + row[1]
        if rtimp_calc > 100:
            row[2] = 100
        else:
            row[2] = rtimp_calc
        cur.updateRow(row)

# create a name for the soils and land use union polygons
arcpy.AddField_management(soils_landuse, "SoilLandUs", "TEXT", 100)

with arcpy.da.UpdateCursor(soils_landuse, [soil_id, landuse_id, "SoilLandUs"]) as cur:
    for row in cur:
        row[2] = '{}: {}'.format(row[0], row[1])
        cur.updateRow(row)
    

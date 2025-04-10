import arcpy

elev_table = arcpy.GetParameterAsText(0)
id_field = arcpy.GetParameterAsText(1)
elev_field = arcpy.GetParameterAsText(2)
x_field = arcpy.GetParameterAsText(3)
y_field = arcpy.GetParameterAsText(4)
dat_path = arcpy.GetParameterAsText(5)

# Create blank .dat files to write GIS data to.
topo = open(dat_path+r'\TOPO.DAT', 'w')

# Loop through elevation table and write data to .dat file
with arcpy.da.SearchCursor(elev_table, [id_field, x_field, y_field, elev_field]) as cursor:
    for row in cursor:
	x = row[1]
	y = row[2]
	z = round(row[3], 2)
	topo.write('%-15s %-15s %s\n' % (x, y, z))

topo.close()

arcpy.AddMessage('DONE!')
                           

        
        
        

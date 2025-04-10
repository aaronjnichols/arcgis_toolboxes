grid = arcpy.GetParameterAsText(0)
id_field = arcpy.GetParameterAsText(1)
rain_path = arcpy.GetParameterAsText(2)

rain_dat = open('{}\RAIN.DAT'.format(rain_path), 'r')
new_rain = open(r'{}\RAIN_new.DAT'.format(rain_path), 'w')

grid_list = []
with arcpy.da.SearchCursor(grid, [id_field]) as cur:
    for row in cur:
        grid_list.append(str(int(row[0])))
    arcpy.AddMessage('{} grids to remove from RAIN.DAT'.format(len(grid_list)))

next(rain_dat)
next(rain_dat)   
for line in rain_dat:
    splt = line.split()
    if splt[0] != 'R' and splt[0] in grid_list:
        new_rain.write('%-14s %-5s\n' % (int(splt[0]), 0))
    else:
    	new_rain.write(line)

new_rain.close()
rain_dat.close()

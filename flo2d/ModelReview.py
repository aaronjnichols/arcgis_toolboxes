import arcpy
import os

# Inputs
grid = arcpy.GetParameterAsText(0)
grid_id = arcpy.GetParameterAsText(1)
f_path = arcpy.GetParameterAsText(2)
vel_threshold = int(arcpy.GetParameterAsText(3))
fr_threshold = int(arcpy.GetParameterAsText(4))


# Create folder
out_path = os.path.join(f_path, 'Model Review Shapefiles')
if os.path.exists(out_path) == False:
    os.makedirs(out_path)
    
# Check if number
def is_number(s):
    try:
        int(s)
        return(True)
    except ValueError:
        return(False)

# Obtain data from output file (cell ID, value)
def ObtainOutputData(f, grid_column, data_column):
    dictionary = {}
    switch = 0
    for line in f:
        splitter = line.split()
        if len(splitter) > 1 and is_number(splitter[grid_column]) == True:
            grid = int(splitter[grid_column])
            data = splitter[data_column]
            dictionary['{}'.format(grid)] =  data
            switch = 1
        elif len(splitter) == 0 and switch == 1:
            break
        else:
            pass
    return(dictionary)

# Create review shapefile with attributes
def CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name):
    grid_string = ",".join("%s" % grid for grid in grid_list)
    arcpy.SelectLayerByAttribute_management(grid, "NEW_SELECTION", '"{}" IN ({})'.format(grid_id, grid_string))
    shp = os.path.join(out_path, new_shp)
    arcpy.CopyFeatures_management(grid, shp)

    # Add fields
    arcpy.AddField_management(shp, field_name, 'FLOAT', 12, 1)
    arcpy.AddField_management(shp, 'Notes', 'TEXT', 200)

    with arcpy.da.UpdateCursor(shp, [grid_id, field_name]) as cursor:
        for row in cursor:
            grid = int(row[0])
            item = dictionary['{}'.format(grid)]
            row[1] = float(item)
            cursor.updateRow(row)

# Process TIME.OUT
time_path = os.path.join(f_path, 'TIME.OUT')
if os.path.exists(time_path) == True:
	time = open(time_path, 'r')
	dictionary = ObtainOutputData(time, 0, 1)
	grid_list = [int(k) for k in dictionary.keys()]
	time.close()
	if len(grid_list) > 0:
		field_name = 'Decrements'
		new_shp = 'TimeDecrements.shp'
		CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name)

# Process EVACUATEDFP.OUT
evac_path = os.path.join(f_path, 'EVACUATEDFP.OUT')
if os.path.exists(f_path+r'\EVACUATEDFP.OUT') == True:
	evac = open(evac_path, 'r')
	dictionary = ObtainOutputData(evac, 0, 1)
	grid_list = [int(k) for k in dictionary.keys()]
	evac.close()
	if len(grid_list) > 0:
		field_name = 'Num_Evac'
		new_shp = 'Evacuations.shp'
		CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name)

# Process VELTIMEFP.OUT
veltimefp_path = os.path.join(f_path, 'VELTIMEFP.OUT')
if os.path.exists(veltimefp_path) == True:
	veltimefp = open(veltimefp_path, 'r')
	dictionary = ObtainOutputData(veltimefp, 0, 1)
	grid_list = [int(k) for k in dictionary.keys() if float(dictionary[k]) > vel_threshold]
	veltimefp.close()
	if len(grid_list) > 0:
		field_name = 'Max_Vel'
		new_shp = 'MaxVelocities.shp'
		CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name)

# Process SUPER.OUT
super_path = os.path.join(f_path, 'SUPER.OUT')
if os.path.exists(super_path) == True:
	super_out = open(super_path, 'r')
	dictionary = ObtainOutputData(super_out, 0, 1)
	grid_list = [int(k) for k in dictionary.keys() if float(dictionary[k]) > fr_threshold]
	super_out.close()
	if len(grid_list) > 0:
		field_name = 'Max_Froude'
		new_shp = 'MaxFroude.shp'
		CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name)

# Process DEPRESSED_ELEMENTS.OUT
depressed_path = os.path.join(f_path, 'DEPRESSED_ELEMENTS.OUT')
if os.path.exists(depressed_path) == True:
	depressed = open(depressed_path, 'r')
	dictionary = ObtainOutputData(depressed, 0, 3)
	grid_list = [int(k) for k in dictionary.keys()]
	arcpy.AddMessage('{} depressed grid elements'.format(len(grid_list)))
	depressed.close()
	if len(grid_list) > 0:
		field_name = 'DepressDep'
		new_shp = 'DepressedElements.shp'
		CreateShapefile(grid_list, new_shp, dictionary, grid, out_path, field_name)

 

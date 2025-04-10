import arcpy

# Inputs
outflow = arcpy.GetParameterAsText(0)
out_id = arcpy.GetParameterAsText(1)
in_id = arcpy.GetParameterAsText(2)
f_path = arcpy.GetParameterAsText(3)
f_name = arcpy.GetParameterAsText(4)

# Create dictionary of upstream (out) and downstream (in) grid ID's
inOutDict = {}
with arcpy.da.SearchCursor(outflow, [out_id, in_id]) as cursor:
    for row in cursor:
        inOutDict[str(int(row[0]))] = int(row[1])

f = open(f_path + r'\OUTNQ.OUT', 'r')
inflow = open(f_path + r'\{}.DAT'.format(f_name), 'w')
time_step = 0.1
switch = 0

# Loop through OUTNQ file and extract hydrographs at outflow cells into dictionary
hydroDict = {}
for line in f:
    splitter = line.split()
    if len(splitter) > 0 and splitter[0] == "ELEMENT":
        switch = 1
    if switch == 1 and len(splitter) > 0 and splitter[0] != "ELEMENT":
        grid = str(splitter[0])
        hydroDict[grid] = [splitter[2]]
        switch = 2
        
    elif switch == 2 and len(splitter) > 0:
        hydroDict[grid].append(splitter[1])

key_list = sorted(hydroDict.keys())
# Loop through the dictionary and write hydrographs with new grid ID's to Inflow DAT file        
for k in key_list:
    if k in inOutDict.keys():
        inflow.write('{:<12} {:>12} {:>12}\n'.format('F', 0, inOutDict[k]))
        t = 0
        switch = 0
        for q in hydroDict[k]:
            inflow.write('{:<12} {:>12} {:>12}\n'.format('H', round(t, 2), q))
            t += time_step
    else:
        pass

f.close()
inflow.close()

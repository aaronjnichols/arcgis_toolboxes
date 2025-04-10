import arcpy

grid_pnts = arcpy.GetParameterAsText(0)
idField = arcpy.GetParameterAsText(1)
arfField = arcpy.GetParameterAsText(2)
IARFBLOCKMOD = arcpy.GetParameterAsText(3)
outPath = arcpy.GetParameterAsText(4)

result = arcpy.GetCount_management(grid_pnts)
count = int(result[0])

arfDAT = open(outPath+r'/ARF.DAT', 'w')
arfDict = {i+1: 0 for i in range(count)}
blockedList = []
with arcpy.da.SearchCursor(grid_pnts, [idField, arfField]) as cursor:
    for row in cursor:
        if round(row[1], 2) < 1 and round(row[1], 2) > 0:
            arfDict[row[0]] = round(row[1], 2)
        elif round(row[1], 2) == 1:
            blockedList.append(row[0])

arfDAT.write('S    {}\n'.format(IARFBLOCKMOD))
for grid in blockedList:
    arfDAT.write('T    {}\n'.format(grid))

for k in arfDict.keys():
    if arfDict[k] > 0:
        arfDAT.write('{:<12}{:<4}    0    0    0    0    0    0    0    0    0\n'.format(k, arfDict[k]))

arfDAT.close()
            
        


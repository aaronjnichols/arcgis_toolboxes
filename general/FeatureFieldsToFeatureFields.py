import arcpy

fcIn = arcpy.GetParameterAsText(0)
matchInField = arcpy.GetParameterAsText(1)
inFields = arcpy.GetParameterAsText(2)
fcOut = arcpy.GetParameterAsText(3)
matchOutField = arcpy.GetParameterAsText(4)
outFields = arcpy.GetParameterAsText(5)

inDict = {}
inFieldList = inFields.split(';')
outFieldList = outFields.split(';')

inFieldList.insert(0, matchInField)
outFieldList.insert(0, matchOutField)    


with arcpy.da.SearchCursor(fcIn, inFieldList) as cursor:
    for row in cursor:
        for i in range(len(inFieldList)-1):
            inDict[str(row[0])] = row[i+1]

with arcpy.da.UpdateCursor(fcOut, outFieldList) as cursor:
    for row in cursor:
        for i in range(len(inFieldList)-1):
            row[i+1] = inDict[str(row[0])][i]
        cursor.updateRow(row)


            
    

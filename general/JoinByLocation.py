import arcpy

class setupJoinByLocation(object):
    def __init__(self):
        self.joinDict = {}
        
    def AddData(self, case, join):
        self.joinDict[str(case)] = join
        
    def getJoinData(self, case):
        return(self.joinDict[str(case)])
    
    def getKeys(self):
        return(list(self.joinDict.keys()))

def JoinByLocation(selectorFC, caseField, selectorField, joinFC, joinField):       
    joinData = setupJoinByLocation()

    with arcpy.da.SearchCursor(selectorFC, [caseField, selectorField]) as cursor:
        for row in cursor:
            joinData.AddData(str(row[0]), row[1])

    keys = joinData.getKeys()
    for k in keys:
	if isinstance(k, (int, float)):
        	arcpy.SelectLayerByAttribute_management(selectorFC, 'NEW_SELECTION', '''"{}" = {} '''.format(caseField, k))
	else:
		arcpy.SelectLayerByAttribute_management(selectorFC, 'NEW_SELECTION', '''"{}" = '{}' '''.format(caseField, k))
        arcpy.SelectLayerByLocation_management(joinFC, 'INTERSECT', selectorFC)
        data = joinData.getJoinData(k)
        arcpy.CalculateField_management(joinFC, joinField, '"{}"'.format(data), 'PYTHON', '')

if __name__ == '__main__':
    # get parameters
    selectorFC = arcpy.GetParameterAsText(0)
    caseField = arcpy.GetParameterAsText(1)
    selectorField = arcpy.GetParameterAsText(2)
    joinFC = arcpy.GetParameterAsText(3)
    joinField = arcpy.GetParameterAsText(4)

    JoinByLocation(selectorFC, caseField, selectorField, joinFC, joinField)




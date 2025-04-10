import arcpy

structures = arcpy.GetParameterAsText(0)
outPath = arcpy.GetParameterAsText(1)

f = open(outPath + r'\HYSTRUC_generalCulvert.DAT', 'w')
fieldsList = ['STRUCTNAME', 'IFPORCHAN', 'ICURVTABLE', 'INFLONOD', 'OUTFLONOD', 'INOUTCONT', 'HEADREFEL', 'CLENGTH', 'CDIAMETER', 'STRUCHAR', 'TYPEC', 'TYPEEN', 'CULVERTN', 'KE', 'CUBASE']
with arcpy.da.SearchCursor(structures, fieldsList) as cursor:
    for row in cursor:
        STRUCTNAME = row[0]
        IFPORCHAN = int(row[1])
        ICURVTABLE = int(row[2])
        INFLONOD = int(row[3])
        OUTFLONOD = int(row[4])
        INOUTCONT = int(row[5])
        HEADREFEL = int(row[6])
        CLENGTH = round(float(row[7]),2)
        CDIAMETER = round(float(row[8]),2)
        STRUCHAR = row[9]
        TYPEC = int(row[10])
        TYPEEN = int(row[11])
        CULVERTN = round(row[12], 3)
        KE = row[13]
        CUBASE = round(float(row[14]),2)

        f.write('S    {}    {}    {}    {}    {}    {}    {}    {}    {}\n'.format(STRUCTNAME, IFPORCHAN, ICURVTABLE, INFLONOD, OUTFLONOD, INOUTCONT, HEADREFEL, CLENGTH, CDIAMETER))
        f.write('     {}    {}    {}    {}    {}    {}\n'.format(STRUCHAR, TYPEC, TYPEEN, CULVERTN, KE, CUBASE))

f.close()

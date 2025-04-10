import arcpy

# ArcGIS Input Parameters
INFIL_PNTS = arcpy.GetParameterAsText(0)
DAT_path = arcpy.GetParameterAsText(1)
id_field = arcpy.GetParameterAsText(2)
xksat_field = arcpy.GetParameterAsText(3)
psif_field = arcpy.GetParameterAsText(4)
dtheta_field = arcpy.GetParameterAsText(5)
abstrinf_field = arcpy.GetParameterAsText(6)
rtimp_field = arcpy.GetParameterAsText(7)
sdepth_field = arcpy.GetParameterAsText(8)

# Create a timer function
def TellTime(t0, tf):
    if tf - t0 < 60:
        arcpy.AddMessage('Run Time = {} seconds.'.format(round(tf-t0,3)))
    else:
        arcpy.AddMessage('Run Time = {} minutes.'.format(round((tf-t0)/60,3)))

# Write INFIL.DAT File
arcpy.AddMessage('\nWriting INFIL.DAT.')
t0 = time.time()
INFIL = open(DAT_path + r'\INFIL.DAT', 'w')
with arcpy.da.SearchCursor(INFIL_PNTS, [id_field, xksat_field, psif_field, dtheta_field, abstrinf_field, rtimp_field, sdepth_field]) as cursor:
    i = 0
    for row in cursor:
        FLO2D_ID = row[0]
        XKSAT = round(float(row[1]), 2)
        PSIF = round(float(row[2]), 2)
        DTHETA = round(float(row[3]), 2)
        ABSTRINF = round(float(row[4]), 2)
        RTIMP = round(float(row[5]), 2)
        S_DEPTH = round(float(row[6]), 2)
        if i == 0:
            # Infiltration Method Line 1
            INFMETHOD = 1

            # Global infiltration parameters Line 2
            ABSTR = 0
            SATI = 0
            SATF = 1
            POROS = 0
            SOILD = S_DEPTH
            INFCHAN = 0

            # Global infiltration parameters Line 3
            HYDCALL = 0
            SOILALL = 0
            HYDCADJ = 0
      
            INFIL.write('%-4s\n' % (INFMETHOD))
            INFIL.write('%-4s %-4s %-4s %-4s %-4s %-4s\n' % (ABSTR, SATI, SATF, POROS, SOILD, INFCHAN))
            INFIL.write('%-4s %-4s %-4s\n' % (HYDCALL, SOILALL, HYDCADJ))
            INFIL.write('F    %-13s %-7s %-8s %-7s %-7s %-7s %-7s\n' % (FLO2D_ID, XKSAT, PSIF, DTHETA, ABSTRINF, RTIMP, S_DEPTH))
        else:
            INFIL.write('F    %-13s %-7s %-8s %-7s %-7s %-7s %-7s\n' % (FLO2D_ID, XKSAT, PSIF, DTHETA, ABSTRINF, RTIMP, S_DEPTH))

        i += 1

INFIL.close()
tf = time.time()
TellTime(t0, tf)
arcpy.AddMessage('\nDONE!')

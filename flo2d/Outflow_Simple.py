f_path = r'C:\Users\anichols\Desktop\Vekol'
f = open(r'{}\OUTFLOW.DAT'.format(f_path), 'w')
outflow_cells = 'FlowExchangeCells'
id_field = 'grid_fid'
location_field = 'OUT_NUM'

with arcpy.da.SearchCursor(outflow_cells, [id_field, location_field]) as cur:
    for row in cur:
        if row[1] == 0:
            f.write('O    {}\n'.format(int(row[0])))
        else:
            f.write('O{}   {}\n'.format(row[1], int(row[0])))

f.close()

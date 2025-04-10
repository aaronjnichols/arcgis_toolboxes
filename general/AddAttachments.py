import csv
import arcpy
import os

# run script
def main():
    
    # get inputs
    fc = arcpy.GetParameterAsText(0)
    fc_field = arcpy.GetParameterAsText(1)
    working_folder = arcpy.GetParameterAsText(2)
    
    match_table = r'C:\temp\matchtable.csv'
    match_field = 'match_field'
    path_field = 'file_name'

    # create a new match table csv file
    writer = csv.writer(open(match_table, 'wb'), delimiter=",")

    # write a header row (the table will have two columns: ParcelID and Picture)
    writer.writerow([match_field, path_field])

    # iterate through each picture in the directory and write a row to the table
    for file in os.listdir(working_folder):
        f = os.path.splitext(file)
        writer.writerow([str(f), file])

    del writer

    # the input feature class must first be GDB attachments enabled
    arcpy.EnableAttachments_management(fc)

    # use the match table with the Add Attachments tool
    arcpy.AddAttachments_management(fc, fc_field, match_table, match_field,
                                    path_field, working_folder)

if __name__ == '__main__':
    main()

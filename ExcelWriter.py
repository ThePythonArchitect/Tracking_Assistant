"""
Even though all of the data is normally
printed to the gui, this class allows the user
to export the data to an excel spreadsheet
"""

#imports
import xlsxwriter


class ExcelWriter:
    """Writes all the data to the Excel file, then opens it.
    """

    def __init__(self, debug):

        self.debug = debug

        return

    def write_file(self, dataset, excel_folder):

        #create our workbook and worksheet
        workbook_name = excel_folder + "\\Time Stamps.xlsx"
        workbook = xlsxwriter.Workbook(workbook_name)
        worksheet = workbook.add_worksheet()
        
        #create the bold format, fill format and set column width
        bold = workbook.add_format({'bold': True})
        fill = workbook.add_format().set_bg_color('gray')
        worksheet.set_column('A:C', 25)

        #write our title cells
        worksheet.write(0, 0, 'Location Name', bold)
        worksheet.write(0, 1, 'Time Arrived', bold)
        worksheet.write(0, 2, 'Time Departed', bold)

        #set the variables to keep track of rows and columns
        row, col = 2, 0

        #write the data to our workbook's worksheet
        for entry in dataset:
            worksheet.write(row, col,         entry.name)
            worksheet.write(row, col + 1, entry.arr_time)
            worksheet.write(row, col + 2, entry.dep_time)
            row += 1

        #close the workbook
        workbook.close()

        return
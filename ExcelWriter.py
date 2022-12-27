import xlwt
import xlrd
from xlutils.copy import copy
import config

class ExcelWriter:
    def __init__(self, name=None) -> None:
        if name != None:
            try:
                rb = xlrd.open_workbook(name)
                self.wb = copy(rb)
            except Exception:
                print("cannot read {}".format(name))
        self.wb = xlwt.Workbook()

    def writeRow(self, data:list, row:int = 0, col:int = 0, sheet=None):
        if sheet == None:
            try:
                wSheet = self.wb.get_sheet(self.wb.get_active_sheet())
            except:
                wSheet = self.wb.add_sheet("New Sheet")
        else:
            wSheet = self.wb.get_sheet(sheet)
            
        for val in data:
            wSheet.write(row, col, val)
            col += 1

    def writeRows(self, data:list, row:int = 0, col:int = 0, sheet=None):
        for rowData in data:
            self.writeRow(rowData,row, col, sheet)
            row += 1

    def saveExcel(self):
        if config.EXCEL_FILE_NAME == "":
            print("can't save. require filename in config")
        fileName = config.EXCEL_FILE_NAME
        self.wb.save(fileName)
        return fileName

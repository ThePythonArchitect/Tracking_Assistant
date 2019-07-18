"""
Tracking-Assistant is an applet that will allow the user
to pull quick reports from their Google Timeline data.


Version 5.0.0

"""

#imports
from FileReader import FileReader
from AddressTranslator import AddressTranslator
from DataCleaner import DataCleaner
from TimeTranslator import TimeTranslator
from ExpenseReport import ExpenseReport
from ExcelWriter import ExcelWriter
from Gui import Gui

#main
class Main:

    def __init__(self):
        
        self.debug = False
        self.debug_FileReader = False
        self.debug_AddressTranslator = False
        self.debug_DataCleaner = False
        self.debug_TimeTranslator = False
        self.debug_ExpenseReport = False
        self.debug_ExcelWriter = False
        self.debug_Gui = False

        return

    def set_full_debug(self, value):

        self.debug = value
        self.debug_FileReader = value
        self.debug_DataCleaner = value
        self.debug_TimeTranslator = value
        self.debug_ExpenseReport = value
        self.debug_ExcelWriter = value
        self.debug_Gui = value

        return

    def run(self):

        addr_translator = AddressTranslator(
            debug=self.debug_AddressTranslator
            )
        reader = FileReader(self.debug_FileReader)
        cleaner = DataCleaner(debug=self.debug_DataCleaner)
        time_translator = TimeTranslator(debug=self.debug_TimeTranslator)
        ex_report = ExpenseReport(debug=self.debug_ExpenseReport)
        ex_writer = ExcelWriter(debug=self.debug_ExcelWriter)

        gui = Gui(debug=self.debug_Gui)
        gui.addr_translator = addr_translator
        gui.reader = reader
        gui.cleaner = cleaner
        gui.time_translator = time_translator
        gui.ex_report = ex_report
        gui.ex_writer = ex_writer

        if self.debug: print("Program start")

        gui.run()

        return


if __name__ == "__main__":
    app = Main()
    app.set_full_debug(True)
    app.run()

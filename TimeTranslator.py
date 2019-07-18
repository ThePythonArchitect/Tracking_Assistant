"""
Responsible for translating the digtial
time stamps to human readable time stamps
"""

#imports
import time


class TimeTranslator:

    def __init__(self, debug):

        self.debug = debug

        return

    def convert(self, timestamp):

        meridiem = 'am'
        month = time.strftime('%b', time.localtime(timestamp))
        day = time.strftime('%d', time.localtime(timestamp))
        if day[0] == 0: day = day[-1] #strip leading 0
        year = time.strftime('%Y', time.localtime(timestamp))
        hour = int(time.strftime('%H', time.localtime(timestamp)))
        minute = time.strftime('%M', time.localtime(timestamp))
        if hour == 12:
            meridiem = 'pm'
        elif hour > 12:
            hour -= 12
            meridiem = 'pm'
        fulltime = f'{month} {day} {year}, {hour}:{minute} {meridiem}'

        return fulltime

    def convert_month(self, timestamp):

        month = time.strftime('%b', time.localtime(timestamp))

        return str(month)

    def convert_day(self, timestamp):

        day = time.strftime('%d', time.localtime(timestamp))
        if day[0] == 0: day = day[-1] #strip leading 0

        return str(day)

    def translate(self, dataset):

        if self.debug: print("Translating dataset")

        translated_data = []

        for entry in dataset:

            entry.arr_month = self.convert_month(entry.arr_time)
            entry.arr_day = self.convert_day(entry.arr_time)
            entry.arr_time = self.convert(entry.arr_time)
            entry.dep_month = self.convert_month(entry.dep_time)
            entry.arr_day = self.convert_day(entry.dep_time)
            entry.dep_time = self.convert(entry.dep_time)

            translated_data.append(entry)

        return translated_data
        
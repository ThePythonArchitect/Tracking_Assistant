"""
Responsible for formatting the data for 
the expense report
"""

#imports
import geopy



class ExpenseReport:

    def __init__(self, debug):

        self.locations = []
        self.debug = debug

        return

    def get_distance(self, location1, location2):
        #returns distance in miles between location 1
        #and location 2

        cords1 = (location1.latitude, location1.longitude)
        cords2 = (location2.latitude, location2.longitude)
        miles = geopy.distance.distance(cords1, cords2).miles

        #precision to the ten's place
        return round(miles, 1)

    def generate(self, dataset):

        #generate from the dataset each day of the month
        #every that the user went (under custom locations)
        #and the miles it is from their previous custom
        #location

        if self.debug:
            print("generating expense report")


        return



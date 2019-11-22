"""
Responsible for formatting the data for 
the expense report
"""

#imports
from geopy.distance import great_circle



class ExpenseReport:

    def __init__(self, debug):

        self.locations = []
        self.debug = debug

        return

    def get_distance(self, location1, location2):
        #returns distance in miles between location 1
        #and location 2

        if self.debug: print("retrieving great circle")

        cords1 = (location1.latitude, location1.longitude)
        cords2 = (location2.latitude, location2.longitude)
        miles = great_circle(cords1, cords2).miles

        if self.debug: print("complete great circle")

        #precision to the ten's place
        return round(miles, 1)

    def generate(self, dataset):

        #generate from the dataset, each day of the month
        #every that the user went (under custom locations)
        #and the miles it is from their previous custom
        #location and group them by day

        if self.debug: print("generating expense report")

        log_file = open("expense_report_debug.txt", "w")
        def log(item):
            item += '\n'
            log_file.write(item)


        #the dictionary that we'll store out sub-day
        #reports in
        expense_report = {}

        #list to contain data for each day
        day_list = []

        #to keep track of our previous entry
        previous_entry = dataset[0]

        #keep track of total miles
        total_miles = 0

        #main for loop to group our data by days
        for x in range(1, len(dataset)):

            log(f"For loop iteration: {x}")

            log(f"Location: {dataset[x].name} | Day: {dataset[x].arr_month} {dataset[x].arr_day}")
            log(f"Previous Location: {previous_entry.name}")

            #check if dataset[x].name is home
            if (dataset[x].name.upper() == "HOME" or
                previous_entry.name.upper() == "HOME"):
                log("Location name or previous location name is home.")

            elif dataset[x].arr_day != previous_entry.arr_day:

                day = dataset[x].arr_month + " " + dataset[x].arr_day
                log(f"New day detected as: {day}.")
                if day_list != []:
                    expense_report[day] = day_list
                    log(f"appended: {day_list} to expense report.")

                #clear the day list
                day_list = []
                log("Day list cleared.")

            else:

                #get mile difference betwen current location
                #and previous location
                miles = self.get_distance(
                    dataset[x],
                    previous_entry
                    )

                log(f"Calculating miles between {dataset[x].name} and {previous_entry.name}.")
                log(f"Miles = {miles}.")

                total_miles += miles
                log(f"total miles incremented to: {total_miles}.")

                #append that info to the day list
                day_list.append([
                    dataset[x].name,
                    miles
                    ])

                log(f"appended day: {dataset[x].arr_month} {dataset[x].arr_day} with {miles} miles to the day list.")

            previous_entry = dataset[x]
            log("Set previous entry.\n")

        log_file.close()

        return []

    def old_generate(self, dataset):

        #generate from the dataset, each day of the month
        #every that the user went (under custom locations)
        #and the miles it is from their previous custom
        #location and group them by day

        if self.debug: print("generating expense report")

        #the dictionary that we'll store out sub-day
        #reports in
        expense_report = {}

        #list to contain data for each day
        day_list = []

        #to keep track of our previous entry
        previous_entry = dataset[0]

        #keep track of total miles
        total_miles = 0

        #main for loop to group our data by days
        for x in range(1, len(dataset)):

            if self.debug: print(f"expense report {x}")

            if (dataset[x].name.upper() == "HOME" and
                previous_entry.name.upper() == "HOME"):

                print("skipped since the current entry or prev entry is home.")

                #skip since miles aren't counted to 
                #from home
                previous_entry = dataset[x]
                continue

            #if we're on a new day in the for loop
            #then append the day list to the expense
            #report and clear the day list
            elif dataset[x].arr_day != previous_entry.arr_day:

                if self.debug: print("generating expense report elif clause")

                #key is the day of the current location
                #value is the day list that was just completed
                day = dataset[x].arr_month + " " + dataset[x].arr_day
                expense_report[day] = day_list

                if self.debug: print(f"appended {day} to expense report.")

                #clear the day list
                day_list = []

            else:

                if self.debug: print("generating expense report: else clause")

                #get mile difference betwen current location
                #and previous location
                miles = self.get_distance(
                    dataset[x],
                    previous_entry
                    )

                total_miles += miles

                #append that info to the day list
                day_list.append([
                    dataset[x].name,
                    miles
                    ])

                if self.debug: print(f"appended {dataset[x].arr_day} with {miles} miles.")

            previous_entry = dataset[x]


        for x in expense_report:
            print(f"{x}: {expense_report[x]}")

        print("done expense report")
        print(f"total miles: {total_miles}")

        return expense_report



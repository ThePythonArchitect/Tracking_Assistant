"""
Responsible for trimming the data and
then cleaning the data.  Re-formatting it
so that it only contains the arrival time
and depature time for each custom location
"""

#imports
import datetime



class DataCleaner:

    def __init__(self, debug):

        #how big in digital latitude and longitude
        #our geo fences will be
        self.geo_size = 0.001
        #set how many minutes a visit to a custom
        #location must exceed to be included in the report
        self.min_minutes = 10 * 60
        #set debug mode
        self.debug = debug

        return

    def set_time_window(self, given_months=1):
        #find epoch time stamp of the beginning of the first day
        #of the month, based of given_months

        if self.debug: print("Setting how many months to show on the report")

        #set epoch
        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)
        #set current date
        current = datetime.datetime.now(datetime.timezone.utc)
        #go back X given months
        month = current.month - (given_months - 1)
        #set year
        year = current.year
        #set our timestamp
        timestamp = datetime.datetime(year, month, 1, 0, 0, 0, 0)
        #calculate our oldest time in epoch
        oldest = (timestamp - epoch).total_seconds()
        #set self.time to our new epoch time stamp
        self.min_months = int(oldest)

        if self.debug: print(f"minimum timestamp: {self.min_months}")

        return

    def in_geofence(self, entry, location):
        #checks if entry is within a geo fence
        #of location

        #set our maximum and minimum for latitude
        lat_max =  location.latitude + self.geo_size
        lat_min =  location.latitude - self.geo_size
        #our maximum and minimum for longitude
        lon_max = location.longitude + self.geo_size
        lon_min = location.longitude - self.geo_size

        #check if entry is in location's geo fence
        if (lat_min < entry.latitude < lat_max and
            lon_min < entry.longitude < lon_max):

            return True

        else:

            return False

        return

    def trim_data(self, dataset, custom_locations):
        #remove all location-time stamps that are older
        #than self.time or that are not within any
        #custom locations' geo fences

        if self.debug: print("Trimming dataset")

        #where we will store our dataset once
        #it has been fully trimmed
        trimmed_dataset = []

        #keep track of last entry
        last_entry = None

        #loop through our data set
        for entry in dataset:

            last_entry = entry

            #if our entry's time stamp too old
            #then skip it
            if entry.time < self.min_months:
                continue

            for location in custom_locations:

                if self.in_geofence(entry, location):
                    #add our location name to our entry
                    entry.name = location.name
                    #then append it to our trimmed_dataset
                    trimmed_dataset.append(entry)

                elif trimmed_dataset[-1].name != "Unknown":
                    entry.name = "Unknown"
                    trimmed_dataset.append(entry)

        return trimmed_dataset

    def clean_data(self, dataset):
        #remove all but the first and last entry
        #in our dataset for each custom location

        if self.debug:
            print("Cleaning dataset")

        #verify that the dataset has at least 1 entry
        if len(dataset) == 0:
            print("No entries in dataset")
            return

        #where we will store our cleaned data
        cleaned_dataset = []

        #keep track of the last location that we saw
        last_entry = dataset[0]

        #keep track of whether we are on an arrival
        #entry or a departure entry
        arrival_entry = dataset[0]

        #loop through all of our data and begin recording
        #the first and last entry for each location and
        #append that to our cleaned list
        for entry in dataset:

            if entry.name != last_entry.name:
                if self.debug:
                    print("Different name found")
                #then we have come across either the
                #first for a new location visit.
                #Therefore we should
                #append it to our cleaned dataset

                #create our arrival and depature times
                arrival_entry.arr_time = arrival_entry.time
                arrival_entry.dep_time = last_entry.time
                #append to our cleaned dataset unless the
                #location was "unknown"
                if last_entry.name != "Unknown":
                    cleaned_dataset.append(arrival_entry)
                    if self.debug:
                        print(f"entry appended: {arrival_entry.name}")
                        print(f"arr time: {arrival_entry.arr_time}")
                        print(f"dep time: {arrival_entry.dep_time}\n")
                #since this is the first entry of this location
                #visit, this entry is our arrival entry
                arrival_entry = entry

            last_entry = entry
        else:
            #finish the last entry
            arrival_entry.arr_time = arrival_entry.time
            arrival_entry.dep_time = last_entry.time
            cleaned_dataset.append(arrival_entry)

        return cleaned_dataset

    def clean_data_min(self, dataset):
        #remove all entry sets that span under
        #our self.min_minutes

        if self.debug: print(
            "Removing false positive entries from dataset"
            )

        cleaned_dataset = []

        for entry in dataset:

            if self.debug:
                print(f"\nminimum cleaning entry: {entry.name}")
                print(f"arrival time: {entry.arr_time}")
                print(f"depature time: {entry.dep_time}")

            difference = entry.dep_time - entry.arr_time

            if difference < self.min_minutes:
                if self.debug:
                    print(f"difference: {difference} less than: {self.min_minutes}")
                continue
            else:
                cleaned_dataset.append(entry)

        return cleaned_dataset

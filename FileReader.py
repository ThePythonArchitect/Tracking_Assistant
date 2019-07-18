"""
FileReader is a class that will open text files and json files.
It then parses the relevant data and returns it.
"""

#imports
import json
import os
from zipfile import ZipFile



class FileReader:

    def __init__(self, debug):
        self.debug = debug
        return

    def extract_archive(self, archive_name):

        #takes the full file path of the archive name
        #extracts the .json file and returns the
        #.json full file path

        if self.debug:
            print("Extracting data from archive")
            print(f"Archive Name: {archive_name}")
        #make sure our archives folder exists
        root_app_dir = os.path.dirname(__file__)
        temp = ""
        for x in root_app_dir:
            if x == "\\":
                temp += "/"
            else:
                temp += x
        root_app_dir = temp
        if "\\" in root_app_dir:
            print("Failed")
            input()
        print(f"root app dir: {root_app_dir}")
        root_app_dir = str(root_app_dir) + "/Archives"
        if not os.path.isdir(root_app_dir):
            os.mkdir(root_app_dir)
        #extract the .json to our archives folder
        with ZipFile(archive_name, "r") as archive:
            listOfFileNames = archive.namelist()
            for fileName in listOfFileNames:
                if fileName.endswith(".json"):
                    archive.extract(fileName, root_app_dir)
                    if self.debug:
                        print(f"{fileName} detected as .json file.")

        return root_app_dir + "/Takeout/Location History/Location History.json"
        
    def read_txt(self):

        if self.debug: print("Reading data from text file")
        #reads data from "Locations.txt" file and returns a list
        #containing [[Location1, address1], [Location2, address2]] etc...
        if not os.path.isfile("Locations.txt"):
            return []
        with open("Locations.txt", 'r') as file:
            lines = file.readlines()

        custom_locations = []

        if self.debug: print(f"{lines} read from file.")

        if lines == None or lines == []:
            assert 1 == 2, "Failed reading from Locations.txt"

        #create a class to store our name and address in
        class Entry:
            def __init__(self, name, address):
                self.name = name
                self.address = address
                return

        for line in lines:
            if line == "" or line == "\n":
                if self.debug: print(f"Line skipped: {line}")
                continue #skip blank lines
            try:
                #client_name equals everything before the first colon
                name = line[0:line.index(':')]
                address = line[line.index(':')+1:]
                address = address.lstrip()
                address = address[:-1] #remove "\n"
                entry = Entry(name=name, address=address)
                custom_locations.append(entry)
            except ValueError:
                print("A line in Locations wasn't formatted correctly.")
                print(f"Line: {line}")

        return custom_locations

    def read_json(self, json_file):
        if self.debug: print("Reading data from json file")
        #reads the "History Location.json" file, then returns it

        #read the json file data and store it in json_data
        try:
            with open(json_file, 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            assert False, "Json file not found"
            
        #strip the data to just the "locations" key
        json_data = json_data['locations']

        #create a list to store our data
        history_locations = []

        #create a class to store our data
        class Entry:
            def __init__(self, time, latitude, longitude):
                self.time = time // 1000
                self.latitude = latitude
                self.longitude = longitude
                return

        #loop through all the json_data and strip everything except
        #the "timestamp", "latutideE7", and "longitudeE7"
        for dictionary in json_data:
            time = int(dictionary["timestampMs"])
            #both of these must be divided by 10 million since
            #Google records them weird?!
            latitude = int(dictionary['latitudeE7']) / 10000000
            longitude = int(dictionary['longitudeE7']) / 10000000
            #create our object
            entry = Entry(
                time=time,
                latitude=latitude,
                longitude=longitude
                )
            #append to our history_locations dictionary
            history_locations.append(entry)

        return history_locations

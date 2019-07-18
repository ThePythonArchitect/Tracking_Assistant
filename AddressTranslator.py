"""
Responsible to translating human readable addresses
into digital latitude, longitude
"""

#imports
import geopy



class AddressTranslator:

    def __init__(self, debug):

        self.debug = debug

        return

    def convert(self, custom_locations):
        if self.debug:
            print("Converting custom locations to digital latitude, longitude")
        #converts the addresses in custom_locations from human readable
        #to longitude and latitude

        #the list we'll return
        converted_locations = []

        #create our encoder agent
        agent = geopy.geocoders.Nominatim(user_agent="Tracking Assistant")

        for entry in custom_locations:
            location = agent.geocode(entry.address)
            entry.latitude = location.latitude
            entry.longitude = location.longitude
            converted_locations.append(entry)

        if self.debug:
            for entry in custom_locations:
                print(f"{entry.name}'s latitude: {entry.latitude}")
                print(f"{entry.name}'s longitude: {entry.longitude}")

        return converted_locations
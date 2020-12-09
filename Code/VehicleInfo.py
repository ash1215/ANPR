import pandas as pd

# vehicle class
class Vehicle:

    # constructor 
    def __init__(self, number):
        self.VehicleNumber = number
        self.Manufacturer = "Unknown"
        self.Owner = "Unknown"
        self.Model = "Unknown"

    def setManufacturer(self, companyName):
        self.Manufacturer = companyName

    def setOwner(self, ownderName):
        self.Owner = ownderName

    def setModel(self, modelName):
        self.Model = modelName

    def getManufacturer(self):
        return self.Manufacturer

    def getOwner(self):
        return self.Owner

    def getModel(self):
        return self.Model

    def getVehicleNumber(self):
        return self.VehicleNumber

    # end constructor

# end class

def GetVehicle(vehicleNumber):
    # reading csv file  
    df = pd.read_csv("VehicleDetails.csv")
    vehicle = Vehicle(vehicleNumber)
    for i in range(len(df)):
        if df["Vehicle Number"][i] == vehicleNumber:
            vehicle.setManufacturer(df["Manufacturer"][i])
            vehicle.setModel(df["Model"][i])
            vehicle.setOwner(df["Owner"][i])
            return vehicle
    return vehicle

class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude
        
    def __eq__(self, other):
        if not isinstance(other, Location):
            return False
        return self.latitude == other.latitude and self.longitude == other.longitude

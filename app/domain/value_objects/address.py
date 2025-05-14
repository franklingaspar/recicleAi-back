class Address:
    def __init__(
        self,
        street: str,
        number: str,
        complement: str,
        neighborhood: str,
        city: str,
        state: str,
        zip_code: str,
    ):
        self.street = street
        self.number = number
        self.complement = complement
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        self.zip_code = zip_code
        
    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return (
            self.street == other.street
            and self.number == other.number
            and self.complement == other.complement
            and self.neighborhood == other.neighborhood
            and self.city == other.city
            and self.state == other.state
            and self.zip_code == other.zip_code
        )

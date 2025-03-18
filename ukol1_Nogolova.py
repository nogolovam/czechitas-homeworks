import math
from abc import ABC, abstractmethod

class Locality:
    def __init__(self, name: str,  locality_coefficient: float):
        self.name = name
        self.locality_coefficient = locality_coefficient

class Property(ABC):
    def __init__(self, locality: Locality):
        self.locality = locality

    @abstractmethod
    def calculate_tax(self):
        pass

class Estate(Property):
    def __init__ (self, locality: Locality, estate_type: str, area:float):
        super().__init__(locality)
        self.estate_type = estate_type
        self.area = area

    def calculate_tax(self):

        if self.estate_type == "land":
            tax = math.ceil(self.area * 0.85 * self.locality.locality_coefficient)
            return tax

        elif self.estate_type == "building site":
            tax = math.ceil(self.area * 9 * self.locality.locality_coefficient)
            return tax

        elif self.estate_type == "forest":
            tax = math.ceil(self.area * 0.35 * self.locality.locality_coefficient)
            return tax

        elif self.estate_type == "garden":
            tax = math.ceil(self.area * 2 * self.locality.locality_coefficient)
            return tax

        else:
            raise ValueError("Wrong estate_type, enter 'land', 'building site', 'forest' or 'garden'")

    def __str__(self):
        if self.estate_type == "land":
            return f"Zemědělský pozemek, lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} metrů čtverečních, daň {self.calculate_tax()} Kč."


        elif self.estate_type == "building site":
            return f"Stavební pozemek, lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} metrů čtverečních, daň {self.calculate_tax()} Kč."


        elif self.estate_type == "forest":
            return f"Les, lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} metrů čtverečních, daň {self.calculate_tax()} Kč."


        elif self.estate_type == "garden":
            return f"Zahrada, lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} metrů čtverečních, daň {self.calculate_tax()} Kč."


class Residence(Property):
    def __init__ (self, locality: Locality, area: float, commercial: bool):
        super().__init__(locality)
        self.locality = locality
        self.area = area
        self.commercial = commercial

    def calculate_tax(self):

        if self.commercial:
            tax = math.ceil((self.area * self.locality.locality_coefficient * 15) * 2)
            return tax

        else:
            tax = math.ceil(self.area * self.locality.locality_coefficient * 15)
            return tax

    def __str__(self):
            return f"Lokalita {self.locality.name} (koeficient {self.locality.locality_coefficient}), {self.area} metrů čtverečních, daň {self.calculate_tax()} Kč."

class TaxReport:
    def __init__(self, name: str,  property_list: list):
        self.name = name
        self.property_list = property_list

    def add_property(self, nemovitost: Estate or Residence):
        self.property_list.append(nemovitost)

    def calculate_tax(self):
        final_tax = 0
        for property in self.property_list:
            final_tax += property.calculate_tax()

        return math.ceil(final_tax)


land = Estate(Locality("Manětín", 0.8), "land", 900)
#print(land.calculate_tax())

house = Residence(Locality("Manětín", 0.8), 120, False)
#print(house.calculate_tax())

office = Residence(Locality("Brno", 3), 90, True)
#print(office.calculate_tax())

#print(office)
#print(land)

taxes = TaxReport("Michaela Nogolová", [land, house])
print(taxes.calculate_tax())

taxes.add_property(office)
print(taxes.calculate_tax())
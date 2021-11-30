
from dataclasses import dataclass
from typing import Optional


@dataclass
class EGRID:

    states: Optional[list] = None
    plant_fuel_types: Optional[list] = None
    layout: Optional[list] = None

    def get_states(self) -> list:
        states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
                  "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
                  "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
                  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
                  "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        self.states = states

    def build_nerc(self) -> dict:

        self.layout = {"NERC": {
            "WECC": ["WA", "OR", "CA", "ID",
                     "NV", "AZ", "MT", "WY",
                     "UT", "CO", "NM"],
            "MRO": ["ND", "SD", "NE", "KS",
                    "OK", "IA", "MN", "WI"],
            "RF": ["MI", "IN", "OH", "PA",
                   "WV", "MD", "DE", "NJ",
                   "DC"],
            "SERC": ["MO", "AR", "LA", "IL", "KY", "VA", "TN", "NC",
                     "SC", "GA", "AL", "MS", "FL"],
            "NPCC": ["NY", "CT", "RI", "MA",
                     "VT", "NH", "ME"],
            "TEXAS": ["TX"],
            "ALASKA": ["AK"],
            "HAWAII": ["HI"],
        }
        }

    def get_plant_fuel_types(self) -> dict:

        self.plant_fuel_types = {
            "hydroelectric": "WAT",
            "bituminous coal": "BIT",
            "subbituminous coal": "SUB",
            "black liquour": "BLQ",
            "tire-derived fuels": "TDF",
            "petroleum coke": "PC",
            "synthetic coal": "SC",
            "biogenic municipal solid waste": "MSB",
            "Disolate Fue Oil": "DFO",
            "Other": "OTH",
            "landfill gas": "LFG",
            "gaseous propane": "PG",
            "waste/other coal": "WC",
            "waste/other oil": "WO",
            "other gas": "OG",
            "kerosene": "KER",
            "residual fuel oil": "RFO",
            "lignite coal": "LIG",
            "other biomass solids": "OBS",
            "jet fuel": "JF",
            "coal-derived synthetic gas": "SGC",
            "blast furnace gas": "BFG",
            "Wind": "WND",
            "Solar": "SUN",
            "Nuclear": "NUC",
            "agricultural by-products": "AB",
            "sludge waste": "SLW",
            "purchased steam": "PUR",
            "other biomass gas": "OBG",
            "subbituminous coal": "SUB",
            "geothermal": "GEO",
            "batteries or other electricity sources": "MWH",
            "waste heat": "WH", "non-biogenic municipal solid waste": "MSN",
            "wood/wood waste solids": "WDS",
            "municipal solid waste": "MSW",
            "Natural Gas": "NG",
            "biogenic municipal solid waste": "MSB",
            "refined coal": "RC",
        }

    def get_plant_fuel_types_tags(self) -> dict:

        self.plant_fuel_type_tags = {
            "WAT": "Hydroelectric",
            "BIT": "Coal",
            "SUB": "Coal",
            "WC": "Coal",
            "LIG": "Coal",
            "SC": "Coal",
            "SGC": "Coal",
            "SUB": "Coal",
            "RC": "Coal",
            "MSB": "Biomass",
            "OBS": "Biomass",
            "LFG": "Biomass",
            "AB": "Biomass",
            "SLW": "Biomass",
            "OBG": "Biomass",
            "WDS": "Biomass",
            "MSB": "Biomass",

            "PG": "Oil Gas",
            "WO": "Oil Gas",
            "OG": "Oil Gas",
            "KER": "Oil Gas",
            "RFO": "Oil Gas",
            "JF": "Oil Gas",
            "BFG": "Oil Gas",
            "BLQ": "Oil Gas",
            "TDF": "Oil Gas",
            "PC": "Oil Gas",
            "DFO": "Oil Gas",

            "WND": "Wind",
            "SUN": "Solar",
            "NUC": "Nuclear",
            "NG": "Natural Gas",



            "GEO": "Geothermal",
            "MWH": "batteries or other electricity sources",

            "MSN": "Municipal Waste",
            "MSW": "Municipal Waste",

            "OTH": "Other",
            "PUR": "Other",
            "WH": "Other",

        }

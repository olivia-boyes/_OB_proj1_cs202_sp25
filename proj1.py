#complete your tasks in this file
#complete your tasks in this file

import math
#task 1
from dataclasses import dataclass

@dataclass(frozen=True)
class GlobeRect:
    lo_lat: float
    hi_lat: float
    west_long: float
    east_long: float

@dataclass(frozen=True)
class Region:
    rect: GlobeRect
    name: str
    terrain: str # "ocean", "mountains", "forest", or "other"

@dataclass(frozen=True)
class RegionCondition:
    region: Region
    year: int
    pop: int
    ghg_rate: float # in tons of CO₂-equivalent per year

#task 2
Seattle_Rect = GlobeRect(47.49, 47.71, 122.4, 122.25)
Seattle_Region = Region(Seattle_Rect, "Seattle", "other")
Seattle_RegionCondition = RegionCondition(Seattle_Region, 2023, 764182, 24200000)

Barca_Rect = GlobeRect(41.26, 41.5, 1.54, 2.18)
Barca_Region = Region(Barca_Rect, "Barcelona", "other")
Barca_RegionCondition = RegionCondition(Barca_Region, 2023, 1700000, 38360000)

Phil_Rect = GlobeRect(0, 30, 120, 150)
Phil_Region = Region(Phil_Rect, "Philippine Sea", "ocean")
Phil_RegionCondition = RegionCondition(Phil_Region, 2024, 112730000,314000000)

SLO_Rect = GlobeRect(35.25, 35.32, 120.62, 120.7)
SLO_Region = Region(SLO_Rect, "San Luis Obispo", "other")
SLO_RegionCondition = RegionCondition(SLO_Region, 2006, 43500, 917700)

region_conditions = [Seattle_RegionCondition, Barca_RegionCondition, Phil_RegionCondition, SLO_RegionCondition]

#task 3
#task 3.1 - make a function that finds how much Co2 is emitted per person per year for a region

def emissions_per_capita(rc: RegionCondition) -> float:
    #should I raise a type error for this function?
    if rc.pop <= 0:
        return 0.0
    return rc.ghg_rate / rc.pop

#task 3.2 - Takes a GlobeRect and returns the estimated surface area of the region in square kilometers.

def area(gr: GlobeRect) -> float:
    R = 6378.1 # Earth's radius in kilometers
    radian_conversion = (math.pi / 180)

    lambda_1 = gr.west_long * radian_conversion
    lambda_2 = gr.east_long * radian_conversion
    psi_1 = gr.lo_lat * radian_conversion
    psi_2 = gr.hi_lat * radian_conversion

    delta_lambda = lambda_2 - lambda_1
    if delta_lambda < 0:
        delta_lambda += 2 * math.pi

    A = (R ** 2) * delta_lambda * abs(math.sin(psi_2) - math.sin(psi_1))

    return A

#task 3.3
# Takes a RegionCondition and returns the tons of CO₂-equivalent per square kilometer.

def emissions_per_square_km(rc: RegionCondition) -> float:
    region_area = area(rc.region.rect)
    if region_area == 0:
        return 0.0
    return rc.ghg_rate / region_area

#task 3.4
# Takes a list of RegionCondition values and returns the name of the region with the highest population density, calculated as: population / area

def densest(rc_list: list[RegionCondition]) -> str:
    # iterate through list and check the region find each population density
    # store the first population density and region name
    # check the following region conditions against the stored region + density
    if len(rc_list) == 0:
        return ""

    initial_region = rc_list[0]
    initial_area: float = area(initial_region.region.rect)
    if initial_area <= 0:
        initial_density = 0.0
    else:
        initial_density = initial_region.pop / initial_area

    def calculate_density(i:int, max_density: float, densest_region: str) -> str:
        if i == len(rc_list):
            return densest_region

        population = rc_list[i].pop
        region_area = area(rc_list[i].region.rect)
        if region_area <= 0:
            density = 0.0
        else:
            density = population / region_area
        if density > max_density:
            max_density = density
            densest_region = rc_list[i].region.name
        return calculate_density(i+1, max_density, densest_region)

    return calculate_density(1, initial_density, initial_region.region.name)


#task 4
#Takes a RegionCondition and a number of years, and returns a new RegionCondition representing the projected state of the region after the given number of years.

def project_condition(rc: RegionCondition, years: int) -> RegionCondition:
    region_terrain = rc.region.terrain

    if region_terrain not in ["ocean", "mountains", "forest", "other"]:
        raise ValueError("The terrain provided is not accepted")

    if region_terrain == "ocean":
        growth_rate = 0.0001
    elif region_terrain == "mountains":
        growth_rate = 0.0005
    elif region_terrain == "forest":
        growth_rate = -0.00001
    else:
        growth_rate = 0.0003

    # new year
    updated_year: int = rc.year + years
    growth_factor = (1 + growth_rate)** years
    # population growth
    updated_pop: int = round(rc.pop * growth_factor)

    # scaled emissions
    updated_ghg_rate: float = rc.ghg_rate * growth_factor

    # new region condition
    updated_region_condition: RegionCondition = RegionCondition(rc.region, updated_year, updated_pop, updated_ghg_rate)

    return updated_region_condition

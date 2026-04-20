import unittest
from proj1 import *
#proj1.py should contain your data class and function definitions
#these do not contribute positively to your grade.
#but your grade will be lowered if they are missing

class TestRegionFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_emissions_per_capita(self):
        Seattle_Rect = GlobeRect(47.49, 47.71, 122.4, 122.25)
        Seattle_Region = Region(Seattle_Rect, "Seattle", "other")
        Seattle_RegionCondition = RegionCondition(Seattle_Region, 2023, 764182, 24200000)

        region0_rect = GlobeRect(0, 1, 0, 1)
        region0_region = Region(region0_rect, "Region 0", "other")
        region0_rc = RegionCondition(region0_region, 2000, 0, 1000)

        self.assertAlmostEqual(emissions_per_capita(Seattle_RegionCondition), 31.6678, 4) #check if functions calculates correctly
        self.assertEqual(emissions_per_capita(region0_rc), 0.0) #check zero population returns 0

    def test_area(self):
        Phil_Rect = GlobeRect(0, 30, 120, 150)
        Negative_East_Long = GlobeRect(0, 30, 170, -170)

        self.assertAlmostEqual(area(Phil_Rect), 10650040.8815, 4)
        self.assertAlmostEqual(area(Negative_East_Long),7100027.25, 2 )

    def test_emissions_per_square_km(self):
        region0_rect = GlobeRect(0, 0, 0, 0)
        region0_region = Region(region0_rect, "Region 0", "other")
        region0_rc = RegionCondition(region0_region, 2000, 0, 1000)

        SLO_Rect = GlobeRect(35.25, 35.32, 120.62, 120.7)
        SLO_Region = Region(SLO_Rect, "San Luis Obispo", "other")
        SLO_RegionCondition = RegionCondition(SLO_Region, 2006, 43500, 917700)

        self.assertEqual(emissions_per_square_km(region0_rc), 0)
        self.assertAlmostEqual(emissions_per_square_km(SLO_RegionCondition), 16200.6, 1 )

    def test_densest(self):
        region_conditions = [Seattle_RegionCondition, Barca_RegionCondition, Phil_RegionCondition, SLO_RegionCondition]

        self.assertEqual(densest(region_conditions), "Barcelona")

    def test_project_condition(self):
        Seattle_Rect = GlobeRect(47.49, 47.71, 122.4, 122.25)
        Seattle_Region = Region(Seattle_Rect, "Seattle", "other")
        Seattle_RegionCondition = RegionCondition(Seattle_Region, 2023, 764182, 24200000)

        Phil_Rect = GlobeRect(0, 30, 120, 150)
        Phil_Region = Region(Phil_Rect, "Philippine Sea", "ocean")
        Phil_RegionCondition = RegionCondition(Phil_Region, 2024, 112730000, 314000000)

        self.assertEqual(project_condition(Seattle_RegionCondition, 10), RegionCondition(Seattle_Region, 2033, 766478, 24272698.088449173))
        self.assertEqual(project_condition(Phil_RegionCondition, 10), RegionCondition(Phil_Region, 2034, 112842781, 314314141.3376866))


if __name__ == '__main__':
    unittest.main()

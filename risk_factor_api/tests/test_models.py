from django.test import TestCase

from risk_factor_api.models import *

class TestInsuranceQuoteModels(TestCase):
    @classmethod
    def setUp(self):
        """Generates data sample that will be used in other methods"""
        self.user_data = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

    def test_generate_marital_status_model(self):
        """Generates a marital status model and check if the data is correct"""
        marital_status_model = MaritalStatus(self.user_data["marital_status"])
        assert marital_status_model == self.user_data["marital_status"]

    def test_generate_ownership_status_model(self):
        """Generates an ownership status model and check if the data is correct"""
        ownership_status_model = HouseOwnerType(self.user_data["house"]["ownership_status"])
        assert ownership_status_model == self.user_data["house"]["ownership_status"]

    def test_generate_risk_profile_plan_model(self):
        """Generates a risk profile plan model and check if the data is correct"""
        risk_profile_plan_model = RiskProfilePlan(
            auto=ProfileSuggestionAfterRisk.ECONOMIC,
            disability=ProfileSuggestionAfterRisk.ECONOMIC,
            home=ProfileSuggestionAfterRisk.ECONOMIC,
            life=ProfileSuggestionAfterRisk.ECONOMIC
        )
        assert risk_profile_plan_model.auto == "economic"
        assert risk_profile_plan_model.disability == "economic"
        assert risk_profile_plan_model.home == "economic"
        assert risk_profile_plan_model.life == "economic"

    def test_generate_house_status_model(self):
        """Generates a house status model and check if the data is correct"""
        house_status_model = HouseStatus(HouseOwnerType(self.user_data["house"]["ownership_status"]))
        assert house_status_model.ownership_status == self.user_data["house"]["ownership_status"]

    def test_generate_vehicle_data_model(self):
        """Generates a vehicle data model and check if the data is correct"""
        vehicle_data_model = VehicleData(year=self.user_data["vehicle"]["year"])
        assert vehicle_data_model.year == self.user_data["vehicle"]["year"]

    def test_generate_user_data_model(self):
        """Generates an user data model and check if the data is correct"""
        user_data_model = UserData(
            age=self.user_data["age"],
            dependents=self.user_data["dependents"],
            house=HouseStatus(HouseOwnerType(self.user_data["house"]["ownership_status"])),
            income=self.user_data["income"],
            marital_status=MaritalStatus(self.user_data["marital_status"]),
            risk_questions=self.user_data["risk_questions"],
            vehicle=VehicleData(year=self.user_data["vehicle"]["year"]),
        )
        assert user_data_model.age == self.user_data["age"]
        assert user_data_model.dependents == self.user_data["dependents"]
        assert user_data_model.house.ownership_status == self.user_data["house"]["ownership_status"]
        assert user_data_model.income == self.user_data["income"]
        assert user_data_model.marital_status == self.user_data["marital_status"]
        assert user_data_model.risk_questions == self.user_data["risk_questions"]
        assert user_data_model.vehicle.year == self.user_data["vehicle"]["year"]
from django.test import TestCase

from risk_factor_api.services import InsuranceService
from risk_factor_api.models import *

class TestInsuranceQuoteService(TestCase):
    @classmethod
    def setUp(self):
        """Generates data sample that will be used in other methods"""
        self.user_data = UserData(
            age=35,
            dependents=2,
            house=HouseStatus(HouseOwnerType.OWNED),
            income=100,
            marital_status=MaritalStatus.MARRIED,
            risk_questions=[0, 1, 0],
            vehicle=VehicleData(year=2018),
        )


    def test_complete_risk_profile_plan(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        profile = InsuranceService().analyze(self.user_data)    
        assert profile.auto == ProfileSuggestionAfterRisk.REGULAR
        assert profile.disability == ProfileSuggestionAfterRisk.ECONOMIC
        assert profile.home == ProfileSuggestionAfterRisk.ECONOMIC
        assert profile.life == ProfileSuggestionAfterRisk.REGULAR

    def test_risk_profile_with_zero_on_all_fields(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.age = 0
        self.user_data.dependents = 0
        self.user_data.house = None
        self.user_data.income = 0
        self.user_data.risk_questions=[0, 0, 0]
        self.user_data.vehicle = None
        profile = InsuranceService().analyze(self.user_data)

        assert profile.auto == ProfileSuggestionAfterRisk.INELIGIBLE
        assert profile.disability == ProfileSuggestionAfterRisk.INELIGIBLE
        assert profile.home == ProfileSuggestionAfterRisk.INELIGIBLE
        assert profile.life == ProfileSuggestionAfterRisk.ECONOMIC


    def test_user_without_car_is_ineligible_for_auto(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.vehicle = None
        profile = InsuranceService().analyze(self.user_data)

        assert profile.auto == ProfileSuggestionAfterRisk.INELIGIBLE


    def test_user_without_house_is_ineligible_for_home(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.house = None
        profile = InsuranceService().analyze(self.user_data)

        assert profile.home == ProfileSuggestionAfterRisk.INELIGIBLE


    def test_user_without_income_is_ineligible_for_disability(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.income = 0
        profile = InsuranceService().analyze(self.user_data)

        assert profile.disability == ProfileSuggestionAfterRisk.INELIGIBLE

    def test_user_under_30_years_is_economic(self):
        self.user_data.age = 20
        profile = InsuranceService().analyze(self.user_data)
        assert profile.auto == ProfileSuggestionAfterRisk.ECONOMIC
        assert profile.disability == ProfileSuggestionAfterRisk.ECONOMIC
        assert profile.home == ProfileSuggestionAfterRisk.ECONOMIC
        assert profile.life == ProfileSuggestionAfterRisk.REGULAR


    def test_user_over_60_year_is_ineligible_for_disability_and_life(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.age = 90
        profile = InsuranceService().analyze(self.user_data)

        assert profile.disability == ProfileSuggestionAfterRisk.INELIGIBLE
        assert profile.life == ProfileSuggestionAfterRisk.INELIGIBLE

    def test_user_with_high_income(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.income = 300000
        profile = InsuranceService().analyze(self.user_data)

        assert profile.auto == ProfileSuggestionAfterRisk.ECONOMIC

    def test_user_house_is_mortgaged(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.house = HouseStatus(HouseOwnerType.MORTGAGED)
        profile = InsuranceService().analyze(self.user_data)

        assert profile.home == ProfileSuggestionAfterRisk.REGULAR

    def test_user_single_without_dependents(self):
        """Calls method analyze passing data and checks if the recommendation is as expected"""
        self.user_data.dependents = 0
        profile = InsuranceService().analyze(self.user_data)
        assert profile.life == ProfileSuggestionAfterRisk.REGULAR

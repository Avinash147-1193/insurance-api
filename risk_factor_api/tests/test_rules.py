from django.test import TestCase

from risk_factor_api.rules import *

class TestInsuranceQuoteRules(TestCase):
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

    def test_less_than_30_years_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.age = 25
        assert 1 == RuleForYoungerThan30(1).calculate(self.user_data)

    def test_less_than_30_years_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 0 == RuleForYoungerThan30(1).calculate(self.user_data)

    def test_between_30_and_40_years_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 1 == RuleForBetween30And40Years(1).calculate(self.user_data)

    def test_between_30_and_40_years_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.age = 25
        assert 0 == RuleForBetween30And40Years(1).calculate(self.user_data)

        self.age = 45
        assert 0 == RuleForBetween30And40Years(1).calculate(self.user_data)

    def test_high_income_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.income = 300000
        assert 1 == RuleForHigherEarning(1).calculate(self.user_data)

    def test_high_income_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 0 == RuleForHigherEarning(1).calculate(self.user_data)

    def test_house_mortgaged_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.house = HouseStatus(HouseOwnerType.MORTGAGED)
        assert 1 == HouseMortgagedRuleStrategy(1).calculate(self.user_data)

    def test_house_mortgaged_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 0 == HouseMortgagedRuleStrategy(1).calculate(self.user_data)

    def test_has_dependents_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 1 == RuleForDependents(1).calculate(self.user_data)

    def test_has_dependents_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.dependents = 0
        assert 0 == RuleForDependents(1).calculate(self.user_data)

    def test_is_married_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 1 == RuleForMaritalStatus(1).calculate(self.user_data)

    def test_is_married_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.marital_status = MaritalStatus.SINGLE
        assert 0 == RuleForMaritalStatus(1).calculate(self.user_data)

    def test_vehicle_has_less_than_5_years_rule_strategy_is_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        assert 1 == VehicleHasLessThan5Years(1).calculate(self.user_data)

    def test_vehicle_has_less_than_5_years_rule_strategy_is_not_applied(self):
        """test passing a score and user data to the rule and checking if it was applied"""
        self.user_data.vehicle = VehicleData(year=1995)
        assert 0 == VehicleHasLessThan5Years(1).calculate(self.user_data)
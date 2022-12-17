from risk_factor_api.models import RiskProfilePlan, ProfileSuggestionAfterRisk
from risk_factor_api.rules import *
from abc import ABC, abstractmethod



class ValueOfRiskForInsurance(ABC):
   #base service class for generating risk points

    def __init__(self):
        self.pointAllocation = []

    def calculate_score(self, user_data):
        #return total score as per input

        score = user_data.base_score()
        for rule in self.pointAllocation:
            score += rule.calculate(user_data)

        return score

    def evaluate(self, user_data):
        #check if user is eligible for an isurance

        if self.check_eligibility(user_data) == False:
            return ProfileSuggestionAfterRisk.INELIGIBLE

        score = self.calculate_score(user_data)
        return self.get_user_profile(score)

    def check_eligibility(self, user_data):
        pass

    def get_user_profile(self, score):
        #Returns instance of ProfileSuggestionAfterRisk based on score

        if score <= 0:
            return ProfileSuggestionAfterRisk.ECONOMIC
        elif score <= 2:
            return ProfileSuggestionAfterRisk.REGULAR
        else:
            return ProfileSuggestionAfterRisk.RESPONSIBLE

class LifeValueOfRiskForInsurance(ValueOfRiskForInsurance):
    #Defines which pointAllocation are applied to Life Insurance profile and what is eligibility criteria.
    #Inherits methods from ValueOfRiskForInsurance.

    def __init__(self):
        self.pointAllocation = [
            RuleForYoungerThan30(-2),
            RuleForBetween30And40Years(-1),
            RuleForHigherEarning(-1),
            RuleForDependents(1),
            RuleForMaritalStatus(1),
        ]

    def check_eligibility(self, user_data):
        return user_data.age <= 60 #less than 60 years is eligibility criteria


class DisabilityValueOfRiskForInsurance(ValueOfRiskForInsurance):
    #Defines which pointAllocation are applied to Disability Insurance profile and what is eligibility criteria.
    #Inherits methods from ValueOfRiskForInsurance.
    
    def __init__(self):
        self.pointAllocation = [
            RuleForYoungerThan30(-2),
            RuleForBetween30And40Years(-1),
            RuleForHigherEarning(-1),
            RuleForDependents(1),
            RuleForMaritalStatus(-1),
        ]

    def check_eligibility(self, user_data):
        #Checks eligibility criteria
        if user_data.house is not None:
            self.pointAllocation.append(HouseMortgagedRuleStrategy(1))
            
        has_income = user_data.income > 0
        is_under_60_years = user_data.age <= 60
        return has_income and is_under_60_years

class HomeValueOfRiskForInsurance(ValueOfRiskForInsurance):
    #Defines which pointAllocation are applied to Home Insurance profile and what is eligibility criteria.
    #Inherits methods from ValueOfRiskForInsurance.

    def __init__(self):
        self.pointAllocation = [
            RuleForYoungerThan30(-2),
            RuleForBetween30And40Years(-1),
            RuleForHigherEarning(-1),
            HouseMortgagedRuleStrategy(1),
        ]

    def check_eligibility(self, user_data):
        #Checks eligibility criteria
        return user_data.house is not None

class AutoValueOfRiskForInsurance(ValueOfRiskForInsurance):
    #Defines which pointAllocation are applied to Auto Insurance profile and what is eligibility criteria.
    #Inherits methods from ValueOfRiskForInsurance.
    def __init__(self):
        self.pointAllocation = [
            RuleForYoungerThan30(-2),
            RuleForBetween30And40Years(-1),
            VehicleHasLessThan5Years(1),
            RuleForHigherEarning(-1),
        ]

    def check_eligibility(self, user_data):
        #Checks eligibility criteria
        return user_data.vehicle is not None

class InsuranceService:
    #Has a method analyze, that receives user data and returns a RiskProfilePlan object.

    def analyze(self, user_data):
        #Builds a RiskProfilePlan with all insurance categories. 
        #Needs to receive user_data as a @dataclass structure. Returns a RiskProfilePlan object.

        return RiskProfilePlan(
            home=HomeValueOfRiskForInsurance().evaluate(user_data),
            auto=AutoValueOfRiskForInsurance().evaluate(user_data),
            life=LifeValueOfRiskForInsurance().evaluate(user_data),
            disability=DisabilityValueOfRiskForInsurance().evaluate(user_data),
            
        )


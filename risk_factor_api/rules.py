from abc import ABC, abstractmethod
from risk_factor_api.models import *

class ScoreCalculation(ABC):
    #Risk Calculation base calss    
    def calculate(self, user_data):
        pass

class RuleForYoungerThan30(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.age < 30:
            return self.__score

        return 0


class RuleForBetween30And40Years(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.age >= 30 and user_data.age <= 40:
            return self.__score

        return 0

class HouseMortgagedRuleStrategy(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.house.ownership_status == HouseOwnerType.MORTGAGED:
            return self.__score

        return 0

class RuleForHigherEarning(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.income > 200000:
            return self.__score

        return 0

class RuleForMaritalStatus(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.marital_status == MaritalStatus.MARRIED:
            return self.__score

        return 0


class VehicleHasLessThan5Years(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.vehicle.years_old() <= 5:
            return self.__score

        return 0


class RuleForDependents(ScoreCalculation):
    def __init__(self, score):
        self.__score = score

    def calculate(self, user_data):
        if user_data.dependents > 0:
            return self.__score

        return 0


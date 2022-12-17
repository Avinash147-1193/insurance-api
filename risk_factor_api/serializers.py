from rest_framework import serializers
from risk_factor_api import models

class QuoteSerializer(serializers.Serializer):
    #Validation for input of the Risk evaluation API
    
    income = serializers.IntegerField(min_value=0)
    age = serializers.IntegerField(min_value=0)
    dependents = serializers.IntegerField(min_value=0)
    
    risk_questions = serializers.ListField(
        child=serializers.IntegerField(
            min_value=0, 
            max_value=1
        ),
        min_length=3, 
        max_length=3
    )

    MARITAL_STATUS_OPTIONS = [
        "single",
        "married",
    ]
    marital_status = serializers.ChoiceField(MARITAL_STATUS_OPTIONS)



    vehicle = serializers.DictField(
        child=serializers.IntegerField(min_value=0),
        required=False, 
    )

    OWNERSHIP_OF_HOUSE_OPTIONS = [
        "owned",
        "mortgaged",
    ]

    house = serializers.DictField(
        child=serializers.ChoiceField(OWNERSHIP_OF_HOUSE_OPTIONS),
        required=False, 
    )
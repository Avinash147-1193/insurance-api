from django.test import TestCase

from risk_factor_api.serializers import QuoteSerializer

class TestInsuranceQuoteSerializers(TestCase):
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

    def test_validate_empty_data(self):
        """try passing empty data and checking if the serializer is valid"""
        self.user_data = {}
        serializer = QuoteSerializer(data=self.user_data)
        assert serializer.is_valid() == False

    def test_validate_incomplete_data(self):
        """try passing incomplete data and checking if the serializer is valid"""
        del self.user_data["age"]
        del self.user_data["dependents"]
        serializer = QuoteSerializer(data=self.user_data)
        assert serializer.is_valid() == False

    def test_validate_complete_data(self):
        """try passing complete data and checking if the serializer is valid"""
        serializer = QuoteSerializer(data=self.user_data)
        assert serializer.is_valid() == True

    def test_validate_wrong_format_data(self):
        """try passing wrong format data and checking if the serializer is valid"""
        self.user_data["dependents"] = "wrong format"
        serializer = QuoteSerializer(data=self.user_data)
        assert serializer.is_valid() == False

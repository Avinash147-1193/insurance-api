from django.shortcuts import render

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from dacite import Config, from_dict
from enum import Enum

import dataclasses, json

from risk_factor_api import serializers, models, services

class QuoteApiView(APIView):
    #Quote API View#
    serializer_class = serializers.QuoteSerializer

    def post(self, request):
        #Create a quote object with user input data#

        if "vehicle" in request.data and request.data["vehicle"] == 0:
            del request.data["vehicle"]
        if "house" in request.data and request.data["house"] == 0:
            del request.data["house"]

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            validated_data = {}
            for key, value in serializer.validated_data.items():
                validated_data[key] = value

            # This is converting the data from a dict to a @dataclass structure
            user_quote_data = from_dict(
                data_class=models.UserData, 
                data=validated_data, 
                config=Config(cast=[Enum])
            )

            analyze_result = services.InsuranceService().analyze(user_quote_data)

            # Before sending it as a response, we need to convert it back to a JSON
            payload = dataclasses.asdict(analyze_result)

            return Response(payload, status=status.HTTP_200_OK)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
             )
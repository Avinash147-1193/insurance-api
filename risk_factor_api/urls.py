from django.urls import path
from risk_factor_api import views

urlpatterns = [
    path('quote/', views.QuoteApiView.as_view(), name='quote'),
]


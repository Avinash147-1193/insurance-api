
from django.conf.urls import url, include

urlpatterns = [
    url(r'^api/', include('risk_factor_api.urls')),
]

from django.urls import path

from currency.views import (
    CurrencyListView
)

urlpatterns = [
    # Auth
    path('all/', CurrencyListView.as_view(), name='all-currency-view'),  
]

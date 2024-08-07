from rest_framework import generics, permissions, response, status

from currency.serializers import CurrencySerializer
from currency.models import Currency

class CurrencyListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CurrencySerializer
    
    def get_queryset(self):
        queryset = Currency.objects.all()
        return queryset
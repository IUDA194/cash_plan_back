from rest_framework import generics, permissions, response, status

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from currency.serializers import CurrencySerializer
from currency.models import Currency

@method_decorator(cache_page(60*15), name='dispatch')  # Кэш на 15 минут
class CurrencyListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CurrencySerializer
    
    def get_queryset(self):
        queryset = Currency.objects.all()
        return queryset
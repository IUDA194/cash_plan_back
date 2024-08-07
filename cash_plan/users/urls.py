from django.urls import path

from users.views import (
    UserLoginView, UserRegisterView, UserDetailView,
    UpdateUserCurrencyView, UpdateUserDailyAmountView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Auth
    path('register/', UserRegisterView.as_view(), name='register'),  
    path('login/', UserLoginView.as_view(), name='login'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh_token'),
    path('profile/', UserDetailView.as_view(), name='user-detail'),
    
    # Settings
    path('settings/update-currency/', UpdateUserCurrencyView.as_view(), name='update-user-currency'),
    path('settings/update-daily-amount/', UpdateUserDailyAmountView.as_view(), name='update-user-daily-amount'),
]

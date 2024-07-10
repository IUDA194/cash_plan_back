from django.urls import path
from plans.views import OperationCreateView, LastOperationsView 

urlpatterns = [
    path('operations/create/', OperationCreateView.as_view(), name='operation-create'),
    path('operations/', LastOperationsView.as_view(), name='user-operations'),

]


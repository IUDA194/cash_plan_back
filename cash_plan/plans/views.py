from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from plans.models import Operation
from plans.serializers import OperationSerializer

class OperationCreateView(generics.CreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LastOperationsView(generics.ListAPIView):
    serializer_class = OperationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        n = self.request.query_params.get('n', None)
        if n is not None:
            n = int(n)
            return Operation.objects.filter(owner=user).order_by('-created_at')[:n]
        return Operation.objects.filter(owner=user).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

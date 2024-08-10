from rest_framework import serializers

from plans.models import Operation

from users.models import User
from users.serializers import UserSerializer

class OperationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Operation
        fields = ['id', 'amount', 'currency', 'owner', 'description', 'created_at']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        user.balance -= amount
        user.save()
        return super().create(validated_data)

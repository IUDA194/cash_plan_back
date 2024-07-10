from rest_framework import serializers
from .models import Operation
from users.models import User

class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ['id', 'amount', 'currency', 'name', 'owner', 'description']
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate(self, data):
        user = self.context['request'].user
        if data['owner'] != user:
            raise serializers.ValidationError("Owner must be the same as the authenticated user.")
        if user.balance < data['amount']:
            raise serializers.ValidationError("Insufficient balance to complete this operation.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        amount = validated_data['amount']
        user.balance -= amount
        user.save()
        return super().create(validated_data)


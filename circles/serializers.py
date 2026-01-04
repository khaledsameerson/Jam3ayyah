from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Circle, Member, Payment, Payout, Notification

# 👇 THIS IS THE MISSING PIECE
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Member
        fields = '__all__'
        # 👇 THIS LINE IS THE FIX. It tells Django "Don't require 'user' in the JSON"
        read_only_fields = ['user', 'balance', 'status']
        
class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source='member.user.username', read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'circle', 'member', 'member_name', 'amount', 'date_paid', 'payment_method', 'transaction_id', 'receipt_image']

class PayoutSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='member.user.username', read_only=True)
    class Meta:
        model = Payout
        fields = ['id', 'circle', 'member', 'username', 'amount', 'date_paid']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class CircleSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)
    payouts = PayoutSerializer(many=True, read_only=True)
    
    class Meta:
        model = Circle
        fields = ['id', 'name', 'monthly_payment', 'duration_months', 'start_date', 'status', 'members', 'payments', 'payouts']
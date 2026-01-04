from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Circle, Member, Payment, Notification

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # This properly hashes the password (security fix)
        user = User.objects.create_user(**validated_data)
        return user

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = Member
        fields = '__all__'
        # 🟢 FIX: This stops the "User field is required" error
        read_only_fields = ['user', 'balance', 'status', 'joined_at']

class CircleSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    payments = serializers.SerializerMethodField()
    payouts = serializers.SerializerMethodField()

    class Meta:
        model = Circle
        fields = '__all__'

    def get_payments(self, obj):
        payments = Payment.objects.filter(circle=obj).order_by('-date_paid')
        return PaymentSerializer(payments, many=True).data

    def get_payouts(self, obj):
        # Simple logic: Return members who have received the pot (status=COMPLETED for now)
        # You can expand this logic later.
        return []

class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.user.username')

    class Meta:
        model = Payment
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
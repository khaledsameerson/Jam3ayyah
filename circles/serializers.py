from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Circle, Member, Payment, Notification

# 1. USER SERIALIZER (First)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# 2. MEMBER SERIALIZER (Second)
class MemberSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = Member
        fields = '__all__'
        read_only_fields = ['user', 'balance', 'status', 'joined_at']

# 3. PAYMENT SERIALIZER (Moved UP! ⬆️)
class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.ReadOnlyField(source='member.user.username')

    class Meta:
        model = Payment
        fields = '__all__'

# 4. NOTIFICATION SERIALIZER
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

# 5. CIRCLE SERIALIZER (Last - Uses PaymentSerializer)
class CircleSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)
    payments = serializers.SerializerMethodField()
    payouts = serializers.SerializerMethodField()

    class Meta:
        model = Circle
        fields = '__all__'

    def get_payments(self, obj):
        # Now this works because PaymentSerializer is already defined above!
        payments = Payment.objects.filter(circle=obj).order_by('-date_paid')
        return PaymentSerializer(payments, many=True).data

    def get_payouts(self, obj):
        return []
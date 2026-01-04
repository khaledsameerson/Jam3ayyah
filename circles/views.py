from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions  # 👈 Added 'permissions' here
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Circle, Member, Payment, Payout, Notification
from .serializers import (
    CircleSerializer, MemberSerializer, PaymentSerializer, 
    PayoutSerializer, RegisterSerializer, NotificationSerializer, UserSerializer
)

# 👇 Make sure your RegisterView looks exactly like this:
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)  # This line will work now!
    serializer_class = RegisterSerializer
# 1. REGISTER
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

# 2. CIRCLES
class CircleViewSet(viewsets.ModelViewSet):
    serializer_class = CircleSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Circle.objects.all()
        return Circle.objects.filter(status='OPEN')

# 3. MEMBERS
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    # 👇 ADD THIS MAGIC METHOD
    def perform_create(self, serializer):
        # This automatically sets 'user' to the person sending the request
        serializer.save(user=self.request.user)

# 4. PAYMENTS (THIS IS THE AUTO-NOTIFICATION ENGINE 🔔)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # A. Save the payment
        payment = serializer.save()
        
        # B. AUTOMATICALLY Create Notifications for everyone
        members = payment.circle.members.all()
        for member in members:
            Notification.objects.create(
                user=member.user,
                message=f"💰 {payment.member.user.username} just paid {payment.amount} JOD!"
            )

# 5. PAYOUTS
class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer
    permission_classes = [permissions.IsAuthenticated]

# 6. NOTIFICATIONS
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user, is_read=False)
    




@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    user = request.user
    user.delete()
    return Response({"message": "Account deleted successfully"}, status=200)
    
# ... your existing code is above ...

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """
    Allows a logged-in user to delete their own account.
    This is required for App Store compliance.
    """
    user = request.user
    user.delete()
    return Response({"message": "Account deleted successfully"}, status=200)
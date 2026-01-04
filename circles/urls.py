from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CircleViewSet, 
    MemberViewSet, 
    PaymentViewSet, 
    PayoutViewSet, 
    NotificationViewSet, 
    RegisterView,
    delete_account  # 👈 Added this missing import!
)

router = DefaultRouter()
router.register(r'circles', CircleViewSet, basename='circle')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payouts', PayoutViewSet, basename='payout')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    # 👇 This line now works because we imported 'delete_account' above
    path('delete-account/', delete_account, name='delete_account'),
]
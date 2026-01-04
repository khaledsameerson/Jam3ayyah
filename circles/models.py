from django.db import models
from django.contrib.auth.models import User

class Circle(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
    ]
    name = models.CharField(max_length=100)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    start_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, related_name='members', on_delete=models.CASCADE)
    # This 'profile_pic' requires Pillow
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"{self.user.username} - {self.circle.name}"

class Payment(models.Model):
    METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CLIQ', 'CliQ'),
        ('BANK', 'Bank Transfer'),
    ]
    circle = models.ForeignKey(Circle, related_name='payments', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='CASH')
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.amount} from {self.member.user.username}"

# 👇 THIS WAS MISSING! The Build Failed because it couldn't find this:
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notif for {self.user.username}: {self.message}"
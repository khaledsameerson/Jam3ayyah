from django.db import models
from django.contrib.auth.models import User

class Circle(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending Approval'), ('OPEN', 'Open'), ('CLOSED', 'Closed')]
    name = models.CharField(max_length=100)
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    duration_months = models.IntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True)
    start_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    def save(self, *args, **kwargs):
        self.total_amount = self.monthly_payment * self.duration_months
        super().save(*args, **kwargs)

class Member(models.Model):
    STATUS_CHOICES = [('PENDING', 'Requested'), ('APPROVED', 'Active'), ('REJECTED', 'Rejected')]
    circle = models.ForeignKey(Circle, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    # ⚠️ Make sure there is NO "class Meta" here blocking duplicates!
class Payment(models.Model):
    circle = models.ForeignKey(Circle, related_name='payments', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, default='CASH')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

class Payout(models.Model):
    circle = models.ForeignKey(Circle, related_name='payouts', on_delete=models.CASCADE)
    member = models.ForeignKey(Member, related_name='received_payouts', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField(auto_now_add=True)

# --- NEW NOTIFICATION SYSTEM 🔔 ---
class Notification(models.Model):
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
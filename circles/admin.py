from django.contrib import admin
from .models import Circle, Payment, Member, Payout, Notification

class CircleAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'monthly_payment')

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'circle', 'status', 'joined_at')
    list_filter = ('status', 'circle')
    actions = ['approve_members']
    def approve_members(self, request, queryset):
        queryset.update(status='APPROVED')

class NotificationAdmin(admin.ModelAdmin): # <--- NEW
    list_display = ('user', 'message', 'is_read', 'created_at')

admin.site.register(Circle, CircleAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Payment)
admin.site.register(Payout)
admin.site.register(Notification, NotificationAdmin) # <--- NEW
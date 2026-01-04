from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('circles.urls')),      # <--- Points to the small map
    path('api-token-auth/', obtain_auth_token), # <--- The Login Door
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('trains.urls')),
    path('api/', include('bookings.urls')),
    path('api/', include('analytics.urls')),
]

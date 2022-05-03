from django.urls import path, include
from django.conf import settings 

urlpatterns = [
    path('planets', include('planets.urls')),
    path('users', include('users.urls')),
    path('bookings', include('bookings.urls')),
    path('wishlists', include('wishlists.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
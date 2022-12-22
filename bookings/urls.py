from django.urls import path

from bookings.views import BookingView, BookingDetailView

urlpatterns = [
    path('', BookingView.as_view()),
    path('/<int:booking_id>', BookingDetailView.as_view()),
]
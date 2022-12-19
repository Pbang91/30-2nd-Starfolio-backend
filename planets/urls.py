from django.urls import path

from planets.views import PlanetsView, PlanetDetailView

urlpatterns = [
    path('', PlanetsView.as_view()),
    path('/<int:planet_id>/accomodation/<int:accomodation_id>', PlanetDetailView.as_view())
]
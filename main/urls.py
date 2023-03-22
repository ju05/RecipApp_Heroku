from django.urls import path
from .views import (
home, profile, update_profile, search, detail, add_recipe, add_to_calendar, add_favorite, favorites_list, signup
)
urlpatterns = [
    path('home', home, name='home'),
    path("update-profile", update_profile, name="update_profile"),
    path("profile", profile, name="profile"),
    path('search', search, name='search'),
    path("detail/<int:id>", detail, name="detail"),
    path("add_favorite/<int:id>", add_favorite, name="add_favorite"),
    path("favorites", favorites_list, name="favorites"),
    path("add_recipe", add_recipe, name="add_recipe"),
    path("add_to_calendar/<int:id>", add_to_calendar, name='add_to_calendar'),
    path("signup", signup, name='signup'),
]
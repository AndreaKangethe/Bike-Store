from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    home, bike_detail, add_to_cart, view_cart, add_review, register,
    add_bike, checkout, increase_quantity, decrease_quantity, profile
)

urlpatterns = [
    path('', home, name='home'),
    path('bike/<int:bike_id>/', bike_detail, name='bike_detail'),
    path('add-to-cart/<int:bike_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('bike/<int:bike_id>/review/', add_review, name='add_review'),
    path('register/', register, name='register'),

    # ✅ Add login & logout URLs
    path('login/', LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),

    path('add-bike/', add_bike, name='add_bike'),
    path('checkout/', checkout, name='checkout'),
    path('cart/increase/<int:item_id>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', decrease_quantity, name='decrease_quantity'),

    # ✅ Add the profile URL
    path('profile/', profile, name='profile'),
]

from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new/", views.new_listing, name="new" ),
    path('<int:listing_id>/', views.listing_page, name='listing'),
    path('<int:listing_id>/place_bid/', views.place_bid, name='place_bid'),
    path('<int:listing_id>/watchlist/', views.watchlist_action, name='watchlist_action'),
    path('<int:listing_id>/toggle_auction/', views.toggle_auction, name='toggle_auction'),
    path('<int:listing_id>/comments/', views.comment, name='comment'),
    path('watchlist/', views.watchlist_page, name='watchlist'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category, name='category'),
    

]


    


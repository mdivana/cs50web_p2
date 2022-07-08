from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('listing/new/', views.ListingCreateView.as_view(), name='listing-create'),
    path('listing/<int:pk>/', views.ListingDetailView.as_view() , name='listing-detail'),
    path('listing/<int:pk>/bid', views.listing_bid, name='listing-bid'),
    path('listing/<int:pk>/comment', views.listing_comment, name='listing-comment'),
    path('listing/<int:pk>/watchlist', views.listing_watchlist, name='listing-watchlist'),
    path('watchlist', views.watchlist_view, name='watchlist'),
    path('category/<str:category>', views.category_view, name='category'),
    path('categories', views.category_list, name='category-list'),
    path('listing/<int:pk>/close', views.listing_close, name='listing-close'),
]
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
]
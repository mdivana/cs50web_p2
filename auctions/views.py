from curses.ascii import HT
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Listing

from .models import User, Listing, Bid, Comment
from .forms import BidForm


def index(request):
    context = {
        'listings': Listing.objects.all()
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    fields = ['title', 'description', 'duration', 'startingbid', 'image_url', 'category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ListingDetailView(LoginRequiredMixin, DetailView):
    model = Listing


@login_required(login_url='/login')
def watchlist_view(request):
    return render(request, "auctions/list_page.html", {
        "auctions" : User.listing_set.all(),
        "title" : "Watchlist"
    })


def add_bid(request, id):
    if request.method == "POST":
        bid_form = BidForm()
        if bid_form.is_valid():
            listing = Listing.objects.get(id=id)
            user = request.user
            new_bid = bid_form.save(commit=False)
            current_bids = Bid.objects.filter(listing=listing)
            highest_bid = all(new_bid.amount > current_bid.amount for current_bid in current_bids)
            valid_bid = new_bid.amount >= listing.start_bid

            if highest_bid and valid_bid:
                new_bid.listing = listing
                new_bid.user = user
                new_bid.save
    url = reverse('listing-detail', kwargs={'pk': id})
    return HttpResponseRedirect(url)

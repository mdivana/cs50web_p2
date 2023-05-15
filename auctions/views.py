from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from .models import User, Listing, Bid, Comment
from .forms import BidForm, CommentForm


def index(request):
    context = {
        'listings': Listing.objects.filter(
            closed = False,
            date_end__gte = datetime.now(),
        ),
        'title': 'Active Listings'
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
    extra_context = {}

    extra_context["Bid"] = Bid
    extra_context["bid_form"] = BidForm()
    extra_context["comment_form"] = CommentForm()

    def get_context_data(self, *args, **kwargs):
        context = super(ListingDetailView, self).get_context_data(*args, **kwargs)
        context["comments"] = Comment.objects.filter(listing_id=self.kwargs['pk'])
        return context


@login_required(login_url='/login')
def listing_bid(request, pk):
    bid_form = BidForm(request.POST or None)
    if bid_form.is_valid():
        listing = Listing.objects.get(id=pk)
        user = request.user
        new_bid = bid_form.save(commit=False)
        try:
            obj = Bid.objects.filter(listing=listing).latest('bid')
            current_bid = Bid._meta.get_field('bid').value_from_object(obj)
            if_higher = new_bid.bid > current_bid
            if_valid = new_bid.bid >= listing.startingbid
            if if_higher and if_valid:
                new_bid.listing = listing
                new_bid.user = user
                new_bid.save()
        except:
            if_valid = new_bid.bid >= listing.startingbid
            if if_valid:
                new_bid.listing = listing
                new_bid.user = user
                new_bid.save()
    return HttpResponseRedirect(reverse('listing-detail', kwargs={'pk': pk}))


@login_required(login_url='/login')
def listing_comment(request, pk):
    comment_form = CommentForm(request.POST or None)
    if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.listing = Listing.objects.get(id=pk)
        new_comment.user = request.user
        new_comment.save()
    return HttpResponseRedirect(reverse('listing-detail', kwargs={'pk': pk}))


@login_required(login_url='/login')
def listing_watchlist(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(id=pk)
        watchlist = request.user.watchlist
        if listing in watchlist.all():
            watchlist.remove(listing)
        else:
            watchlist.add(listing)
    return HttpResponseRedirect(reverse('listing-detail', kwargs={'pk': pk}))


@login_required(login_url='/login')
def watchlist_view(request):
    return render(request, "auctions/index.html", {
        "listings": request.user.watchlist.all(),
        "title": "Watchlist"
    })


@login_required(login_url='/login')
def category_view(request, category):
    context = {
        'listings': Listing.objects.filter(
            category = category,
            closed = False,
            date_end__gte = datetime.now(),
            ),
        'title': category,
    }
    return render(request, "auctions/index.html", context)


def category_list(request):
    context = {
        'categories': Listing.objects.values_list('category', flat=True).distinct(),
    }
    return render(request, "auctions/category_list.html", context)


def listing_close(request, pk):
    if request.method == "POST":
        listing = Listing.objects.get(id=pk)
        if request.user == listing.author:
            listing.closed = True
            listing.save()
    return HttpResponseRedirect(reverse('listing-detail', kwargs={'pk': pk}))